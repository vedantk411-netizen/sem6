import sys
import os

# Add static folder to path so we can import the manager
sys.path.append(os.path.join(os.getcwd(), 'static'))

try:
    from backend_mongo_manager import add_drive_image_to_collection, add_new_shoot_type
except ImportError:
    print("Error: Could not import backend_mongo_manager. Make sure you are running this from the project root.")
    sys.exit(1)

# 1. Ensure 'Wedding' collection exists
add_new_shoot_type("Wedding")

# 2. Add the specific Drive Folder link
folder_link = "https://drive.google.com/drive/folders/1Qf54Wd3D1s6ILZCAl1_2mWNLZaux5iuK?usp=sharing"
name = "Wedding Portfolio (Drive Folder)"

success = add_drive_image_to_collection("Wedding", name, folder_link)

if success:
    print("Successfully saved the Wedding Drive Folder link to MongoDB!")
else:
    print("Failed to save the link.")