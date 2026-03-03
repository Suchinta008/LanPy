DEV_MODE = True
import time
from app.core.discovery import PeerDiscovery
from app.core.messaging import MessagingServer, send_message
from app.core.port_check import is_udp_port_available, find_free_tcp_port
from app.core.config import UDP_DISCOVERY_PORT, TCP_MESSAGING_PORT
from app.core.instance_lock import SingleInstance
from app.core.database import ChatDatabase
from PyQt5.QtWidgets import QApplication
import sys
from app.ui.main_window import MainWindow
from app.ui.setup_dialog import SetupDialog

def main():
    app = QApplication(sys.argv)
    instance = None
    db = ChatDatabase()

    if not DEV_MODE:
        instance = SingleInstance()
        try:
            instance.acquire()
        except RuntimeError as e:
            print(f"❌ {e}")
            return

    tcp_port = find_free_tcp_port(TCP_MESSAGING_PORT)
    print(f"✔ TCP Messaging Port Selected: {tcp_port}")

    # Check DB for saved username
    username = db.get_saved_username()

    if not username:
        setup = SetupDialog()
        if setup.exec_():
            username = setup.get_username()
            if not username:
                print("Username cannot be empty")
                return
            db.save_username(username)
        else:
            return

    discovery = PeerDiscovery(username, tcp_port)
    discovery.start()

    messaging = MessagingServer(username, tcp_port, db)
    messaging.start()

    # ---- GUI START ----

    window = MainWindow(username, discovery, messaging, db)
    window.show()

    exit_code = app.exec_()

    discovery.stop()
    messaging.stop()

    if instance:
        instance.release()

    sys.exit(exit_code)
# def main():
#     # Single instance
#     instance = None
#     db = ChatDatabase()

#     if not DEV_MODE:
#         instance = SingleInstance()
#         try:
#             instance.acquire()
#         except RuntimeError as e:
#             print(f"❌ {e}")
#             return

#     # UDP fixed
#     # if not is_udp_port_available(UDP_DISCOVERY_PORT):
#     #     print(f"❌ UDP port {UDP_DISCOVERY_PORT} is already in use.")
#     #     return

#     # Dynamic TCP
#     tcp_port = find_free_tcp_port(TCP_MESSAGING_PORT)
#     print(f"✔ TCP Messaging Port Selected: {tcp_port}")

#     username = input("Enter username: ")

#     # Start discovery
#     discovery = PeerDiscovery(username, tcp_port)
#     discovery.start()

#     # Start messaging server
#     messaging = MessagingServer(username, tcp_port, db)
#     messaging.start()

#     # Start Qt Application
#     app = QApplication(sys.argv)

#     window = MainWindow(username, discovery, messaging, db)
#     window.show()

#     exit_code = app.exec_()

#     # Cleanup when window closes
#     discovery.stop()
#     messaging.stop()

#     if instance:
#         instance.release()

#     sys.exit(exit_code)

#     # try:
#     #     while True:
#     #         print("\nActive peers:")
#     #         peers = discovery.get_peers()

#     #         for ip, info in peers.items():
#     #             print(f"{ip} -> {info}")

#     #         target_key = input("\nEnter target (ip:port) or press Enter to refresh: ").strip()

#     #         if target_key in peers:
#     #             peer = peers[target_key]
#     #             text = input("Enter message: ")

#     #             send_message(
#     #                 peer["ip"],          # real IP
#     #                 peer["tcp_port"],    # correct TCP port
#     #                 username,
#     #                 text,
#     #                 db
#     #             )

#     #         elif target_key:
#     #             print("❌ Invalid target selected.")

#     #         time.sleep(1)

#     # except KeyboardInterrupt:
#     #     discovery.stop()
#     #     messaging.stop()
#     #     if instance:
#     #         instance.release()


if __name__ == "__main__":
    main()