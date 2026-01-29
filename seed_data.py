from pymongo import MongoClient
import bcrypt

def seed_database():
    # Connect to MongoDB
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['photomind']
        print("Connected to MongoDB.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return

    # --- 1. Bulk Insert Lighting Rules & Camera Settings ---
    lighting_rules_collection = db['lighting_rules']
    
    # Define the rules data
    rules_data = [
        # Wedding
        {"shoot_type": "Wedding", "rule": "Golden Hour: Schedule couple portraits 1 hour before sunset for soft, warm light."},
        {"shoot_type": "Wedding", "rule": "Indoor Reception: Use bounce flash off ceilings/walls to avoid harsh shadows."},
        {"shoot_type": "Wedding", "rule": "Camera Settings: Aperture f/2.8-f/4 for depth of field, Shutter 1/200s minimum for moving subjects."},
        
        # Portrait
        {"shoot_type": "Portrait", "rule": "Rembrandt Lighting: Position key light 45 degrees to the side and above subject."},
        {"shoot_type": "Portrait", "rule": "Eyes: Ensure catchlights are visible in the subject's eyes."},
        {"shoot_type": "Portrait", "rule": "Camera Settings: 85mm lens, f/1.8 for bokeh, ISO 100 for clarity."},

        # Outdoor
        {"shoot_type": "Outdoor", "rule": "Overcast Days: Great for soft, even lighting without harsh shadows."},
        {"shoot_type": "Outdoor", "rule": "Mid-day Sun: Find open shade (under trees/buildings) to avoid raccoon eyes."},
        {"shoot_type": "Outdoor", "rule": "Camera Settings: ISO 100-400, f/8 for landscapes, f/2.8 for isolated subjects."},

        # Event
        {"shoot_type": "Event", "rule": "Low Light: Use fast prime lenses (f/1.4 or f/1.8)."},
        {"shoot_type": "Event", "rule": "Crowds: Raise camera high or use a wide angle to capture the atmosphere."},
        {"shoot_type": "Event", "rule": "Camera Settings: ISO 1600-3200, Shutter 1/125s to freeze motion."},

        # Product
        {"shoot_type": "Product", "rule": "Softbox: Use large light sources for smooth gradients on reflective surfaces."},
        {"shoot_type": "Product", "rule": "Background: Use a seamless white sweep (infinity curve) for clean isolation."},
        {"shoot_type": "Product", "rule": "Camera Settings: f/11-f/16 for full sharpness, Tripod is mandatory."},

        # Night
        {"shoot_type": "Night", "rule": "Long Exposure: Use a tripod and remote shutter release."},
        {"shoot_type": "Night", "rule": "Cityscapes: Shoot during 'Blue Hour' (just after sunset) for balanced sky and city lights."},
        {"shoot_type": "Night", "rule": "Camera Settings: ISO 100-800, f/8-f/11, Shutter 2s-30s."},

        # Fashion
        {"shoot_type": "Fashion", "rule": "Hard Light: Use direct sunlight or bare strobes for edgy, high-contrast looks."},
        {"shoot_type": "Fashion", "rule": "Movement: Use a fan for hair/fabric movement."},
        {"shoot_type": "Fashion", "rule": "Camera Settings: f/5.6-f/8 to keep clothes in focus, Shutter 1/500s+."}
    ]

    # Insert rules if they don't exist (simple check to avoid massive duplication on re-run)
    if lighting_rules_collection.count_documents({}) == 0:
        lighting_rules_collection.insert_many(rules_data)
        print(f"Inserted {len(rules_data)} lighting rules.")
    else:
        print("Lighting rules collection is not empty. Skipping bulk insert to avoid duplicates.")

    # --- 2. Auto-Register Dummy Photographers ---
    photographers_collection = db['photographers']
    
    dummies = [
        {"name": "Alice Lens", "email": "alice@example.com", "password": "password123"},
        {"name": "Bob Shutter", "email": "bob@example.com", "password": "password123"},
        {"name": "Charlie ISO", "email": "charlie@example.com", "password": "password123"}
    ]

    count = 0
    for user in dummies:
        if not photographers_collection.find_one({"email": user['email']}):
            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
            
            photographers_collection.insert_one({
                "name": user['name'],
                "email": user['email'],
                "password": hashed_password,
                "role": "photographer"
            })
            count += 1
            print(f"Created user: {user['email']}")
    
    if count == 0:
        print("Dummy users already exist.")
    else:
        print(f"Registered {count} new dummy photographers.")

if __name__ == "__main__":
    seed_database()