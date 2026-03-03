import socket
import threading
import time
import json
from typing import Dict

from PyQt5.QtCore import QObject, pyqtSignal
from app.core.config import UDP_DISCOVERY_PORT


BROADCAST_INTERVAL = 5
PEER_TIMEOUT = 15
BUFFER_SIZE = 4096


class PeerDiscovery(QObject):
    username_conflict = pyqtSignal(str)

    def __init__(self, username: str, tcp_port: int):
        super().__init__()

        self.username = username
        self.tcp_port = tcp_port

        self.peers: Dict[str, dict] = {}
        self.lock = threading.Lock()

        self.listener_thread = None
        self.broadcast_thread = None
        self.cleanup_thread = None

        self.running = False

    # ==========================================================
    # PUBLIC METHODS
    # ==========================================================

    def start(self):
        self.running = True

        print(f"[DISCOVERY] Starting on UDP {UDP_DISCOVERY_PORT}")

        self.listener_thread = threading.Thread(
            target=self._listen, daemon=True
        )
        self.broadcast_thread = threading.Thread(
            target=self._broadcast_loop, daemon=True
        )
        self.cleanup_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True
        )

        self.listener_thread.start()
        self.broadcast_thread.start()
        self.cleanup_thread.start()

    def stop(self):
        self.running = False

    def get_peers(self):
        with self.lock:
            return dict(self.peers)

    # ==========================================================
    # INTERNAL METHODS
    # ==========================================================

    def _listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Allow multiple instances on same machine
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except (AttributeError, OSError):
            pass

        try:
            sock.bind(("", UDP_DISCOVERY_PORT))
        except OSError as e:
            print(f"❌ Failed to bind UDP {UDP_DISCOVERY_PORT}: {e}")
            return

        print(f"[DISCOVERY] Listening on UDP {UDP_DISCOVERY_PORT}")

        while self.running:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                message = json.loads(data.decode())

                if message.get("type") != "DISCOVERY":
                    continue

                sender_ip = addr[0]
                sender_port = message.get("tcp_port")
                sender_username = message.get("username")

                # Ignore own broadcast
                if (
                    sender_username == self.username
                    and sender_port == self.tcp_port
                ):
                    continue

                peer_key = f"{sender_ip}:{sender_port}"

                with self.lock:
                    self.peers[peer_key] = {
                        "ip": sender_ip,
                        "username": sender_username,
                        "tcp_port": sender_port,
                        "last_seen": time.time(),
                    }

            except Exception as e:
                print("[DISCOVERY] Listen error:", e)

    def _broadcast_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        print("[DISCOVERY] Broadcasting started")

        while self.running:
            try:
                message = json.dumps({
                    "type": "DISCOVERY",
                    "username": self.username,
                    "tcp_port": self.tcp_port,
                })

                # Windows-safe broadcast
                sock.sendto(
                    message.encode(),
                    ("255.255.255.255", UDP_DISCOVERY_PORT)
                )

                # Localhost (for same machine testing)
                sock.sendto(
                    message.encode(),
                    ("127.0.0.1", UDP_DISCOVERY_PORT)
                )

            except Exception as e:
                print("[DISCOVERY] Broadcast error:", e)

            time.sleep(BROADCAST_INTERVAL)

    def _cleanup_loop(self):
        while self.running:
            time.sleep(5)
            now = time.time()

            with self.lock:
                inactive = [
                    key
                    for key, info in self.peers.items()
                    if now - info["last_seen"] > PEER_TIMEOUT
                ]

                for key in inactive:
                    print(f"[DISCOVERY] Removing inactive peer: {key}")
                    del self.peers[key]