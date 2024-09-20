import os
import sqlite3
from cryptography.fernet import Fernet

class DatabaseHandler:
    def __init__(self, database_name: str, key: bytes):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row
        self.cipher_suite = Fernet(key)

    def user_init(self, member_id: int):
        cursor = self.con.cursor()
        query = "INSERT INTO user_table (id_user) VALUES (?);"
        cursor.execute(query, (member_id,))
        cursor.close()
        self.con.commit()

    def check_data(self, member_id: int) -> bool:
        cursor = self.con.cursor()
        query = "SELECT * FROM user_table WHERE id_user = ?;"
        cursor.execute(query, (member_id,))
        result = cursor.fetchall()
        cursor.close()
        return len(result) == 1

    def add_user(self, user_id, username, password, url):
        cursor = self.con.cursor()
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        encrypted_username = self.cipher_suite.encrypt(username.encode())
        query = "INSERT INTO pronote_users (id, username, password, url) VALUES (?, ?, ?, ?);"
        cursor.execute(query, (user_id, encrypted_username, encrypted_password, url))
        cursor.close()
        self.con.commit()

    def get_user_info(self, user_id):
        cursor = self.con.cursor()
        query = "SELECT username, password, url FROM pronote_users WHERE id=?;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        if result:
            encrypted_username, encrypted_password, url = result[0]
            username = self.cipher_suite.decrypt(encrypted_username).decode()
            password = self.cipher_suite.decrypt(encrypted_password).decode()
            return username, password, url
        return None
