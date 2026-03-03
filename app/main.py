import sys
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("LAN P2P Chat - Environment Ready 🚀")
label.resize(300, 100)
label.show()
sys.exit(app.exec_())