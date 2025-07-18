import sqlite3
from datetime import datetime
import os
from pathlib import Path

class Database:
    def __init__(self, db_name="ip_records.db"):
        # Получаем путь к директории, где находится database.py
        base_dir = Path(__file__).parent
        # Создаём папку db, если она не существует
        db_dir = base_dir / "db"
        db_dir.mkdir(exist_ok=True)
        # Формируем полный путь к базе данных
        db_path = db_dir / db_name
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS ip_records (
                    ip TEXT PRIMARY KEY,
                    note TEXT,
                    created_at TEXT
                )
            """)

    def check_ip(self, ip):
        cursor = self.conn.cursor()
        cursor.execute("SELECT note, created_at FROM ip_records WHERE ip = ?", (ip,))
        return cursor.fetchone()

    def save_ip(self, ip, note):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO ip_records (ip, note, created_at) VALUES (?, ?, ?)",
                (ip, note, datetime.now().isoformat())
            )
