"""
Seed shoot types into MongoDB so all types (including Sports) appear in the UI.
Run: python seed_shoot_types.py
"""
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['photomind']
shoot_types_collection = db['shoot_types']

shoot_types = [
    {'name': 'Wedding', 'icon': 'fas fa-heart', 'description': 'Weddings & ceremonies', 'created_at': datetime.now()},
    {'name': 'Portrait', 'icon': 'fas fa-user', 'description': 'Portrait sessions', 'created_at': datetime.now()},
    {'name': 'Event', 'icon': 'fas fa-calendar', 'description': 'Corporate & social events', 'created_at': datetime.now()},
    {'name': 'Product', 'icon': 'fas fa-box', 'description': 'Product and e-commerce', 'created_at': datetime.now()},
    {'name': 'Landscape', 'icon': 'fas fa-mountain', 'description': 'Landscape and nature', 'created_at': datetime.now()},
    {'name': 'Fashion', 'icon': 'fas fa-tshirt', 'description': 'Fashion and editorial', 'created_at': datetime.now()},
    {'name': 'Sports', 'icon': 'fas fa-basketball-ball', 'description': 'Sports and action photography', 'created_at': datetime.now()},
]

for st in shoot_types:
    existing = shoot_types_collection.find_one({'name': st['name']})
    if existing:
        print(f"Skipped existing: {st['name']}")
    else:
        shoot_types_collection.insert_one(st)
        print(f"Inserted: {st['name']}")

print('Seeding complete.')
