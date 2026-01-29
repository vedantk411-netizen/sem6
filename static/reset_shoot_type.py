from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["photomind"]

SHOOT_TYPE = "Wedding"  # The collection you want to clear

if SHOOT_TYPE in db.list_collection_names():
    # Delete all documents in the collection
    result = db[SHOOT_TYPE].delete_many({})
    print(f"Deleted {result.deleted_count} items from '{SHOOT_TYPE}' collection.")
    print("You can now run the bulk_add_drive_images.py script again.")
else:
    print(f"Collection '{SHOOT_TYPE}' does not exist.")