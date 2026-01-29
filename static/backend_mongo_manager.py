import os
from pymongo import MongoClient

# Configuration
# Ensure you have a running MongoDB instance
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "photomind"
STATIC_FOLDER = os.path.join(os.getcwd(), 'static')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_data_for_shoot_type(shoot_type):
    """
    Fetches data specifically from the collection named after the shoot_type.
    Example: If shoot_type is 'Wedding', it queries the 'Wedding' collection.
    """
    if shoot_type not in db.list_collection_names():
        return {"rules": [], "poses": []}
    
    collection = db[shoot_type]
    
    # Fetch rules and poses from this specific collection
    rules = list(collection.find({"category": "rule"}, {"_id": 0}))
    
    # Fetch poses (supports both local 'image_path' and remote 'image_url')
    poses = list(collection.find({"category": "pose"}, {"_id": 0}))
    
    return {"rules": rules, "poses": poses}

def add_new_shoot_type(shoot_type_name):
    """
    1. Creates a specific folder for the shoot type in the static directory.
    2. Creates a new MongoDB collection for the shoot type.
    """
    # Sanitize name to be safe for filesystem and database
    safe_name = "".join(x for x in shoot_type_name if x.isalnum() or x in " -_").strip()
    
    if not safe_name:
        raise ValueError("Invalid shoot type name")

    # 1. Create specific folder
    folder_path = os.path.join(STATIC_FOLDER, safe_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

    # 2. Create MongoDB collection (Lazy creation: inserting a document creates it)
    if safe_name not in db.list_collection_names():
        db.create_collection(safe_name)
        # Insert a metadata document to initialize the collection
        db[safe_name].insert_one({"info": "collection_init", "type": safe_name})
        print(f"Created MongoDB collection: {safe_name}")
        
        # 3. Ensure it exists in the global 'shoot_types' collection (for Dashboard/Portfolio visibility)
        shoot_types_col = db['shoot_types']
        if not shoot_types_col.find_one({"name": shoot_type_name}):
            shoot_types_col.insert_one({
                "name": shoot_type_name,
                "icon": "fas fa-camera", # Default icon
                "description": f"Gallery for {shoot_type_name}"
            })
            print(f"Added '{shoot_type_name}' to global shoot_types list.")
        return True
    else:
        print(f"Collection {safe_name} already exists")
        return False

def add_drive_image_to_collection(shoot_type, name, drive_link, category="pose"):
    """
    Stores a Google Drive link in the specific shoot type collection.
    """
    if shoot_type not in db.list_collection_names():
        print(f"Error: Collection '{shoot_type}' does not exist. Create it first.")
        return False

    # specific collection for this shoot type
    collection = db[shoot_type]

    # Basic logic to convert a standard share link to a direct view link if needed
    # (This assumes the user provides a standard Google Drive ID or link)
    final_url = drive_link
    if "drive.google.com/file/d/" in drive_link:
        file_id = drive_link.split("/d/")[1].split("/")[0]
        # Use thumbnail endpoint which is more reliable for embedding images
        final_url = f"https://lh3.googleusercontent.com/d/{file_id}"
    elif "drive.google.com/drive/folders/" in drive_link:
        # It is a folder link, keep it as is
        final_url = drive_link

    document = {
        "name": name,
        "image_url": final_url,  # The link to the image
        "category": category,
        "source": "google_drive",
        "shoot_type": shoot_type
    }

    collection.insert_one(document)
    print(f"Added Drive image '{name}' to collection '{shoot_type}'")
    return True