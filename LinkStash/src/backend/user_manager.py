# src/backend/user_manager.py

import bcrypt
from pymongo import MongoClient
import os


class UserManager:
    def __init__(self):
        password = os.environ.get("MONGO_PWD")
        self.client = MongoClient(
            f"mongodb+srv://Rudraksh:{password}@cluster0.1hsclqh.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"
        )
        self.db = self.client["linkstash"]
        self.collection = self.db["users"]

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password, hashed):
        return bcrypt.checkpw(password.encode("utf-8"), hashed)

    def create_user(self, username, password):
        if self.collection.find_one({"username": username}):
            raise ValueError("Username already exists.")
        self.collection.insert_one(
            {"username": username, "password_hash": self.hash_password(password)}
        )

    def login(self, username, password):
        user = self.collection.find_one({"username": username})
        if user and self.check_password(password, user["password_hash"]):
            return str(user["_id"])
        return None
