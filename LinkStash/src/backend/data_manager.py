from pymongo import MongoClient
from datetime import datetime
import bson
import os
import sys

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


load_dotenv(resource_path(".env"))


class LinkManager:
    def __init__(self, user_id):
        if not user_id:
            raise ValueError("user_id must be provided to LinkManager.")

        try:
            self.user_id = bson.ObjectId(user_id)
            self.password = os.environ.get("MONGO_PWD")
            self.client = MongoClient(
                f"mongodb+srv://Rudraksh:{self.password}@cluster0.1hsclqh.mongodb.net/?retryWrites=true&w=majority&tls=true"
            )
            self.db = self.client["linkstash"]
            self.collection = self.db["links"]
            self.collection.create_index("url")
            self.collection.create_index("notes")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def add_link(self, url, notes=""):
        existing = self.collection.find_one({"url": url, "user_id": self.user_id})

        if not existing:
            self.collection.insert_one(
                {
                    "url": url,
                    "notes": notes,
                    "saved_at": datetime.now().isoformat(),
                    "user_id": self.user_id,
                }
            )

    def get_links(self, search_term=""):
        query = {"user_id": self.user_id}
        if search_term:
            query = {
                "$or": [
                    {"url": {"$regex": search_term, "$options": "i"}},
                    {"notes": {"$regex": search_term, "$options": "i"}},
                ]
            }
        return [
            {
                "_id": str(doc["_id"]),
                "url": doc["url"],
                "notes": doc.get("notes", ""),
                "saved_at": doc["saved_at"],
            }
            for doc in self.collection.find(query)
        ]

    def delete_link(self, link_id):
        self.collection.delete_one(
            {
                "_id": bson.ObjectId(link_id),
                "user_id": self.user_id,
            }
        )

    def update_link(self, link_id, new_url, new_notes=""):
        self.collection.update_one(
            {"_id": bson.ObjectId(link_id), "user_id": self.user_id},
            {
                "$set": {
                    "url": new_url,
                    "notes": new_notes,
                    "saved_at": datetime.now().isoformat(),
                }
            },
        )

    def close(self):
        self.client.close()


if __name__ == "__main__":
    link_manager = LinkManager(user_id="demo_user")
    try:
        links = link_manager.get_links()
        for link in links:
            print(
                f"ID: {link['_id']}, URL: {link['url']}, Notes: {link['notes']}, Saved At: {link['saved_at']}"
            )
    finally:
        link_manager.close()
