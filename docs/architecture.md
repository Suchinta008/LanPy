# 1. Network Discovery Layer

Uses UDP broadcast:

    Client → Broadcast → WHO_IS_ONLINE
    
    Peers → Reply → USER:<username>:<ip>

# 2. Messaging Layer

Direct TCP connection:

    Sender → TCP → Receiver

# 3. File Transfer Layer

TCP chunk-based transfer:

    Metadata packet

    File chunks

    Completion flag

# 4. Local Storage

Each client stores its own SQLite database.

## Communication Flow

1️⃣ On startup:

    Start UDP listener

    Start TCP listener

    Broadcast discovery

2️⃣ On message send:

    Open TCP socket

    Send JSON

    Close socket

3️⃣ On file send:

    Open TCP socket

    Send file metadata

    Send chunks

    Close socket
