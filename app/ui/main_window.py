import time
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QTextEdit, QLineEdit, QPushButton,
    QLabel, QListWidgetItem, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, username, discovery, messaging, db):
        super().__init__()

        self.username = username
        self.discovery = discovery
        self.messaging = messaging
        self.db = db

        self.peer_map = {}
        self.active_chat_user = None

        self.setWindowTitle(f"LAN Chat - {username}")
        self.resize(1100, 650)

        self._build_ui()
        self._apply_dark_theme()

        # Signals
        self.messaging.message_received.connect(self.display_incoming_message)
        self.peer_list.itemClicked.connect(self.open_chat)

        # Auto refresh peers
        self._start_peer_refresh()

    # ==========================================================
    # UI BUILD
    # ==========================================================

    def _build_ui(self):

        main_container = QWidget()
        self.setCentralWidget(main_container)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_container.setLayout(main_layout)

        # -------------------------
        # LEFT ICON BAR
        # -------------------------
        icon_bar = QFrame()
        icon_bar.setFixedWidth(70)

        icon_layout = QVBoxLayout()
        icon_layout.setAlignment(Qt.AlignTop)
        icon_layout.setSpacing(25)
        icon_layout.setContentsMargins(0, 40, 0, 0)

        icon_bar.setLayout(icon_layout)

        icon_layout.addWidget(QLabel("💬", alignment=Qt.AlignCenter))

        main_layout.addWidget(icon_bar)

        # -------------------------
        # CHAT LIST PANEL
        # -------------------------
        chat_list_container = QFrame()
        chat_list_container.setFixedWidth(280)

        chat_list_layout = QVBoxLayout()
        chat_list_layout.setContentsMargins(15, 20, 15, 20)

        chat_list_container.setLayout(chat_list_layout)

        title = QLabel("Messages")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        chat_list_layout.addWidget(title)

        self.peer_list = QListWidget()
        chat_list_layout.addWidget(self.peer_list)

        main_layout.addWidget(chat_list_container)

        # -------------------------
        # CHAT AREA
        # -------------------------
        self.chat_container = QFrame()
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(25, 20, 25, 20)
        self.chat_container.setLayout(chat_layout)

        # Header
        self.header_container = QHBoxLayout()

        self.avatar_placeholder = QLabel()
        self.header_container.addWidget(self.avatar_placeholder)

        self.chat_header = QLabel("Select a chat")
        self.chat_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.header_container.addWidget(self.chat_header)

        self.status_dot = QLabel()
        self.status_dot.setFixedSize(10, 10)
        self.status_dot.setStyleSheet("""
            background-color: #00c853;
            border-radius: 5px;
        """)
        self.header_container.addWidget(self.status_dot)

        self.header_container.addStretch()

        self.clear_btn = QPushButton("Clear Chat")
        self.clear_btn.setFixedHeight(28)
        self.clear_btn.clicked.connect(self.clear_chat)
        self.header_container.addWidget(self.clear_btn)

        chat_layout.addLayout(self.header_container)

        # Message area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.hide()
        chat_layout.addWidget(self.chat_area)

        # Input container
        self.input_container = QFrame()
        bottom_layout = QHBoxLayout()
        self.input_container.setLayout(bottom_layout)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        bottom_layout.addWidget(self.message_input)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        bottom_layout.addWidget(send_btn)

        self.input_container.hide()
        chat_layout.addWidget(self.input_container)

        main_layout.addWidget(self.chat_container)

    # ==========================================================
    # AVATAR
    # ==========================================================

    def _create_avatar(self, name, size=36):
        first_letter = name[0].upper()
        color = "#2a9df4"

        avatar = QLabel(first_letter)
        avatar.setFixedSize(size, size)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(f"""
            background-color: {color};
            color: white;
            border-radius: {size//2}px;
            font-weight: bold;
            font-size: 14px;
        """)
        return avatar

    # ==========================================================
    # THEME
    # ==========================================================

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f1720;
                color: #e6e6e6;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QListWidget {
                background-color: #111b21;
                border: none;
                padding: 5px;
            }

            QListWidget::item {
                padding: 12px;
                border-radius: 8px;
            }

            QListWidget::item:selected {
                background-color: #202c33;
            }

            QTextEdit {
                background-color: #0f1720;
                border: none;
                padding: 15px;
            }

            QLineEdit {
                background-color: #202c33;
                border-radius: 20px;
                padding: 10px 15px;
                border: none;
            }

            QPushButton {
                background-color: #2a9df4;
                border-radius: 20px;
                padding: 8px 18px;
                color: white;
            }

            QPushButton:hover {
                background-color: #1e88e5;
            }
        """)

    # ==========================================================
    # DISCOVERY
    # ==========================================================

    def _start_peer_refresh(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_peers)
        self.timer.start(3000)

    def refresh_peers(self):
        peers = self.discovery.get_peers()

        self.peer_list.clear()
        self.peer_map = {}

        for key, info in peers.items():
            username = info["username"]

            # if username == self.username:
            #     continue

            self.peer_map[username] = {
                "ip": info["ip"],
                "tcp_port": info["tcp_port"]
            }

            item = QListWidgetItem(username)
            self.peer_list.addItem(item)

    # ==========================================================
    # CHAT HANDLING
    # ==========================================================

    def open_chat(self, item):
        username = item.text()
        self.active_chat_user = username

        self.chat_header.setText(username)

        # Replace avatar
        avatar = self._create_avatar(username)
        self.avatar_placeholder.setParent(None)
        self.avatar_placeholder = avatar
        self.header_container.insertWidget(0, avatar)

        self.chat_area.show()
        self.input_container.show()
        self.chat_area.clear()

        history = self.db.get_chat_history(self.username, username)

        for sender, receiver, message, ts in history:
            if sender == self.username:
                self._append_bubble(message, align="right", timestamp=ts)
            else:
                self._append_bubble(message, align="left", timestamp=ts)

    def send_message(self):

        if not self.active_chat_user:
            return

        peer = self.peer_map.get(self.active_chat_user)
        if not peer:
            return

        text = self.message_input.text()
        if not text:
            return

        from app.core.messaging import send_message

        send_message(
            peer["ip"],
            peer["tcp_port"],
            self.username,
            text,
            self.db
        )

        self._append_bubble(text, align="right", timestamp=time.time())
        self.message_input.clear()

    def display_incoming_message(self, sender, text):
        if sender != self.active_chat_user:
            return
        self._append_bubble(text, align="left")

    # ==========================================================
    # BUBBLES
    # ==========================================================

    def _append_bubble(self, text, align="left", timestamp=None):

        if timestamp:
            time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M")
        else:
            time_str = datetime.now().strftime("%H:%M")

        if align == "right":
            bubble_color = "#2a9df4"
            align_style = "right"
        else:
            bubble_color = "#1f2c34"
            align_style = "left"

        html = f"""
            <div style="text-align:{align_style}; margin-top:6px; margin-bottom:6px;">
                <div style="
                    display:inline-block;
                    background:{bubble_color};
                    padding:10px 14px;
                    border-radius:18px;
                    max-width:60%;
                    text-align:left;
                    word-wrap:break-word;
                ">
                    <div>{text}</div>
                    <div style="
                        font-size:10px;
                        opacity:0.7;
                        margin-top:4px;
                        text-align:right;
                    ">
                        {time_str}
                    </div>
                </div>
            </div>
        """

        self.chat_area.append(html)

        # Auto scroll
        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )

        

    # ==========================================================
    # CLEAR CHAT
    # ==========================================================
    def clear_chat(self):
        if not self.active_chat_user:
            return

        reply = QMessageBox.question(
            self,
            "Clear Chat",
            f"Are you sure you want to clear chat with {self.active_chat_user}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Delete from DB
            self.db.clear_chat(self.username, self.active_chat_user)

            # Clear UI
            self.chat_area.clear()