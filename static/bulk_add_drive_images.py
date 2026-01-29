import sys
import os

# Add static folder to path so we can import the manager
sys.path.append(os.path.join(os.getcwd(), 'static'))

try:
    from backend_mongo_manager import add_drive_image_to_collection, add_new_shoot_type
except ImportError:
    print("Error: Could not import backend_mongo_manager. Make sure you are running this from the project root.")
    sys.exit(1)

# --- CONFIGURATION ---
SHOOT_TYPE = "Wedding"  # Change this to your shoot type (e.g., "Portrait", "Event")

# PASTE YOUR LINKS BELOW
# These must be individual image links (e.g., ending in 'view?usp=sharing')
LINKS = [
    "https://drive.google.com/file/d/1W19UZDDHOM8K1DLsVoGmhSI31xqM2Vzp/view?usp=drive_link",
    "https://drive.google.com/file/d/1D5dRGNpN76ZcrArl_uTmZdkz1YpjZlSh/view?usp=drive_link",
    "https://drive.google.com/file/d/1Qf7WPoL4yTCCjAOi9cU_NsKt9WO1PjaQ/view?usp=drive_link",
    "https://drive.google.com/file/d/1wXFyl-p-oO_5kkRCUdsu00d9hrDgg-ep/view?usp=drive_link",
    # Add as many links as you want here...
]

def main():
    print(f"--- Bulk Adding Images to '{SHOOT_TYPE}' ---")
    
    # 1. Ensure the collection exists
    add_new_shoot_type(SHOOT_TYPE)
    
    count = 0
    for i, link in enumerate(LINKS):
        if "drive.google.com" not in link:
            print(f"Skipping invalid link: {link}")
            continue
            
        # Generate a name (e.g., "Wedding Image 1")
        name = f"{SHOOT_TYPE} Image {i+1}"
        
        # Add to MongoDB
        add_drive_image_to_collection(SHOOT_TYPE, name, link)
        count += 1
        
    print(f"\nSuccessfully added {count} images to the '{SHOOT_TYPE}' collection.")

if __name__ == "__main__":
    main()