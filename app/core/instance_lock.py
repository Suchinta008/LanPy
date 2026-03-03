import socket


class SingleInstance:
    def __init__(self, lock_port: int = 50999):
        self.lock_port = lock_port
        self.socket = None

    def acquire(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Bind only to localhost
            self.socket.bind(("127.0.0.1", self.lock_port))
        except OSError:
            raise RuntimeError("LAN P2P Chat is already running.")

    def release(self):
        if self.socket:
            self.socket.close()