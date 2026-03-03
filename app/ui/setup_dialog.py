from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton
)


class SetupDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Setup Username")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Enter your username:"))

        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        self.save_button = QPushButton("Continue")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

    def get_username(self):
        return self.username_input.text().strip()