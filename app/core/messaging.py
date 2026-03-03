import socket
import threading
import json
import time
from app.core.config import BUFFER_SIZE
from PyQt5.QtCore import QObject, pyqtSignal

class MessagingServer(QObject):
    message_received = pyqtSignal(str, str)
    
    def __init__(self, username: str, tcp_port: int, db):
        super().__init__()
        self.username = username
        self.tcp_port = tcp_port
        self.db = db
        self.running = False
        self.server_socket = None

    # =========================
    # Start TCP Listener
    # =========================

    def start(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", self.tcp_port))
        self.server_socket.listen()

        thread = threading.Thread(target=self._accept_loop, daemon=True)
        thread.start()

        print(f"✔ Messaging server listening on port {self.tcp_port}")

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()

    # =========================
    # Accept Incoming Connections
    # =========================

    def _accept_loop(self):
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                thread = threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                thread.start()
            except Exception:
                continue

    # =========================
    # Handle Incoming Message
    # =========================

    def _handle_client(self, conn, addr):
        try:
            data = conn.recv(BUFFER_SIZE)
            message = json.loads(data.decode())

            if message.get("type") == "MESSAGE":
                sender = message["sender"]
                text = message["text"]

                # Save to DB
                self.db.save_message(sender, self.username, text)

                # Emit signal to GUI
                self.message_received.emit(sender, text)

        except Exception:
            pass
        finally:
            conn.close()


# =========================
# Client Send Function
# =========================

def send_message(target_ip, target_port, sender, text, db):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))

        payload = json.dumps({
            "type": "MESSAGE",
            "sender": sender,
            "text": text,
            "timestamp": time.time()
        })

        sock.sendall(payload.encode())
        sock.close()

        # Save sent message
        db.save_message(sender, f"{target_ip}:{target_port}", text)

    except Exception as e:
        print(f"❌ Failed to send message: {e}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))

        payload = json.dumps({
            "type": "MESSAGE",
            "sender": sender,
            "text": text,
            "timestamp": time.time()
        })

        sock.sendall(payload.encode())
        sock.close()

    except Exception as e:
        print(f"❌ Failed to send message: {e}")