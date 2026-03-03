# LanPy - A P2P Chat (Serverless Office Messenger)

A lightweight peer-to-peer LAN chat application built in Python.
No central server required. Works only inside the same network.

## Features
- Automatic LAN user discovery (UDP broadcast)
- Direct peer-to-peer messaging (TCP)
- File sharing
- Local chat history storage
- No internet required
- Cross-platform (Windows/Linux)

## Architecture
- UDP Broadcast → User discovery
- TCP → Message & file transfer
- SQLite → Local chat history

## Installation

1. Clone repository
2. Install requirements:
   pip install -r requirements.txt
3. Run:
   python app/main.py

## Build EXE
   pyinstaller --onefile --windowed app/main.py