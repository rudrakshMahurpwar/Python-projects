from pymongo import MongoClient
from datetime import datetime
import bson


class LinkManager:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client["linkstash"]
            self.collection = self.db["links"]
            self.collection.create_index("url")
            self.collection.create_index("notes")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def add_link(self, url, notes=""):
        if url:
            self.collection.insert_one(
                {"url": url, "notes": notes, "saved_at": datetime.now().isoformat()}
            )

    def get_links(self, search_term=""):
        query = {}
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
        self.collection.delete_one({"_id": bson.ObjectId(link_id)})

    def update_link(self, link_id, new_url, new_notes=""):
        self.collection.update_one(
            {"_id": bson.ObjectId(link_id)},
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
    link_manager = LinkManager()
    try:
        links = link_manager.get_links()
        for link in links:
            print(
                f"ID: {link['_id']}, URL: {link['url']}, Notes: {link['notes']}, Saved At: {link['saved_at']}"
            )
    finally:
        link_manager.close()
