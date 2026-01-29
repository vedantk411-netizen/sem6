#!/usr/bin/env python
"""Fix image paths in MongoDB - add 'static/' prefix to old paths"""

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['photomind']

# Update all photos with old path format (uploads/ -> static/uploads/)
result = db['analyzed_photos'].update_many(
    {'image_path': {'$regex': '^uploads/'}},
    [{'$set': {'image_path': {'$concat': ['static/', '$image_path']}}}]
)

print(f'✓ Matched: {result.matched_count}, Modified: {result.modified_count}')

# Verify the update
photos = list(db['analyzed_photos'].find().sort('_id', -1).limit(3))
print(f'\n✓ Latest {len(photos)} photos:')
for photo in photos:
    print(f"  - {photo['image_path']}")
