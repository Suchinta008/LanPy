import sqlite3
import threading
import time


class ChatDatabase:
    def __init__(self, db_name="chat_history.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.lock = threading.Lock()
        self._create_table()

    def _create_table(self):
        with self.lock:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT,
                    receiver TEXT,
                    message TEXT,
                    timestamp REAL
                )
            """)
            self.conn.commit()

    def save_message(self, sender, receiver, message):
            with self.lock:
                self.conn.execute("""
                    INSERT INTO messages (sender, receiver, message, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (sender, receiver, message, time.time()))
                self.conn.commit()

    def get_chat_history(self, user1, user2):
        with self.lock:
            cursor = self.conn.execute("""
                SELECT sender, receiver, message, timestamp
                FROM messages
                WHERE (sender=? AND receiver=?)
                OR (sender=? AND receiver=?)
                ORDER BY timestamp ASC
            """, (user1, user2, user2, user1))

            return cursor.fetchall()
        
    def get_saved_username(self):
        cursor = self.conn.execute("""
            CREATE TABLE IF NOT EXISTS user_config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.conn.commit()

        cursor = self.conn.execute(
            "SELECT value FROM user_config WHERE key='username'"
        )
        row = cursor.fetchone()
        return row[0] if row else None


    def save_username(self, username):
        self.conn.execute("""
            INSERT OR REPLACE INTO user_config (key, value)
            VALUES ('username', ?)
        """, (username,))
        self.conn.commit()

    def clear_chat(self, user1, user2):
        with self.lock:
            self.conn.execute("""
                DELETE FROM messages
                WHERE (sender = ? AND receiver = ?)
                OR (sender = ? AND receiver = ?)
            """, (user1, user2, user2, user1))

            self.conn.commit()