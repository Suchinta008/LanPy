# 🚀 LanPY

### Peer-to-Peer LAN Chat Application (Python + PyQt5)

[![Latest Release](https://img.shields.io/github/v/release/Suchinta008/LanPy?style=flat\&color=blue)](https://github.com/Suchinta008/LanPy/releases)
[![Downloads](https://img.shields.io/github/downloads/Suchinta008/LanPy/total?color=brightgreen)](https://github.com/Suchinta008/LanPy/releases)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat\&logo=python\&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?style=flat\&logo=qt\&logoColor=white)](https://pypi.org/project/PyQt5/)
[![SQLite](https://img.shields.io/badge/SQLite-Local%20Database-003B57?style=flat\&logo=sqlite\&logoColor=white)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## ⬇️ Download Latest Release

👉 **[Download LanPY for Windows](https://github.com/Suchinta008/LanPy/releases/latest)**

No installation required. Just download and run.

---

## 🧠 Overview

LanPY is a lightweight peer-to-peer LAN chat application built using Python and PyQt5.

It enables devices connected to the same local network to:

* 🔍 Automatically discover each other
* 💬 Communicate in real-time
* 💾 Store chat history locally
* 🎨 Use a modern Telegram-inspired UI
* 👤 Maintain persistent usernames
* 🧹 Clear conversations anytime

No internet required.
No central server.
Fully decentralized within the local network.

---

# 🏗 System Architecture

```
User A                         User B
--------                       --------
UDP Broadcast  <----------->  UDP Listener
     |                                |
TCP Messaging <----------->   TCP Server
     |                                |
SQLite (Local DB)           SQLite (Local DB)
```

### 🔹 Peer Discovery

* UDP Broadcast on port `5001`
* Automatic LAN peer detection
* Unique peer key using `IP:PORT`

### 🔹 Messaging

* TCP socket-based communication
* Dynamic port allocation
* Real-time message delivery

### 🔹 Persistence

* SQLite local database
* Chat history storage
* Username saved locally for future sessions

---

# ✨ Features

* 🔎 Automatic LAN peer discovery (UDP)
* 💬 Real-time messaging (TCP)
* 🗂 Persistent chat history (SQLite)
* 🎨 Modern dark-themed UI
* 👤 Unique username validation within network
* 🟢 Online status indicator
* 🧹 Clear chat functionality
* 🔄 Multi-instance support (Development mode)
* 📦 Windows executable build via PyInstaller

---

# 📸 Screenshots

Add screenshots inside `assets/screenshots/`:

```
assets/screenshots/
    ├── main_ui.png
    ├── chat_example.png
```

Then include:

```
![Main UI](assets/screenshots/main_ui.png)
![Chat Example](assets/screenshots/chat_example.png)
```

---

# 📂 Project Structure

```
LanPy/
│
├── app/
│   ├── core/
│   │   ├── discovery.py
│   │   ├── messaging.py
│   │   ├── database.py
│   │   ├── port_check.py
│   │   └── instance_lock.py
│   │
│   ├── ui/
│   │   ├── main_window.py
│   │   └── setup_dialog.py
│   │
│   └── main.py
│
├── assets/
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙️ Installation (Run From Source)

## 1️⃣ Clone Repository

```
git clone https://github.com/Suchinta008/LanPy.git
cd LanPy
```

## 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

## 4️⃣ Run Application

```
python -m app.main
```

---

# 🔌 Networking Details

| Component        | Protocol | Port         |
| ---------------- | -------- | ------------ |
| Peer Discovery   | UDP      | 5001         |
| Messaging Server | TCP      | 5002+ (auto) |

* TCP port auto-relocates if busy
* UDP alerts user if port unavailable

---

# 🛠 Build Executable

Using PyInstaller:

```
pyinstaller --onefile --windowed --name LanPY app/main.py
```

Output:

```
dist/LanPY.exe
```

---

# 🧪 Development Mode

Supports running multiple instances on the same machine:

* Dynamic TCP port selection
* Localhost UDP broadcast enabled
* Useful for testing without multiple devices

---

# 🚀 Future Roadmap

* 📁 File sharing over LAN
* 📎 Drag & drop file sending
* 🖼 Media preview support
* 🔐 End-to-end message encryption (AES)
* 🔔 System tray support
* 📦 Linux AppImage build
* 🌐 Cross-platform client (Flutter / React Native)
* ⚙️ Auto-update mechanism

---

# 🧠 Design Philosophy

* No external servers
* No cloud storage
* Lightweight & efficient
* Fully local-first communication
* Clean and modern UI

---

# 📝 Changelog

## v1.0.0 – Initial Release

* UDP peer discovery
* TCP real-time messaging
* SQLite persistence
* Modern UI implementation
* Clear chat feature
* Windows executable build

---

# 👨‍💻 Author

**Suchinta Chanda**
📧 [suchintachanda@gmail.com](mailto:suchintachanda@gmail.com)

---

# 📜 License

MIT License

---