"""
Seed MongoDB with environment-specific lighting rules for each shoot type.
Now includes INDOOR and OUTDOOR environment tags for targeted suggestions.
"""

from pymongo import MongoClient, errors
from datetime import datetime

try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client['photomind']
    lighting_rules_collection = db['lighting_rules']
    print("✓ Connected to MongoDB")
except errors.ConnectionFailure as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# Clear existing rules (optional - comment out to preserve)
lighting_rules_collection.delete_many({})
print("✓ Cleared existing lighting rules")

# Environment-specific lighting rules for each shoot type
rules = [
    # ============== WEDDING ==============
    # INDOOR Wedding
    {
        'shoot_type': 'Wedding',
        'environment': 'indoor',
        'category': 'lighting',
        'rule': 'Use soft, diffused light with minimal harsh shadows for elegant indoor ceremonies',
        'camera_settings': {'iso': 3200, 'aperture': 1.4, 'shutter': '1/250'}
    },
    {
        'shoot_type': 'Wedding',
        'environment': 'indoor',
        'category': 'gear',
        'rule': 'Use fast prime lenses (24mm, 35mm, 50mm f/1.4) for low-light performance',
        'camera_settings': {'lenses': '24mm f/1.4, 35mm f/1.4, 50mm f/1.4'}
    },
    {
        'shoot_type': 'Wedding',
        'environment': 'indoor',
        'category': 'composition',
        'rule': 'Capture intimate moments close to the couple with shallow depth of field',
        'camera_settings': {'aperture': 1.4, 'focus_mode': 'single_point'}
    },
    {
        'shoot_type': 'Wedding',
        'environment': 'indoor',
        'category': 'focus',
        'rule': 'Use continuous AF (AI Servo/AF-C) for moving subjects during ceremonies',
        'camera_settings': {'af_mode': 'continuous', 'af_tracking': 'enabled'}
    },
    # OUTDOOR Wedding
    {
        'shoot_type': 'Wedding',
        'environment': 'outdoor',
        'category': 'lighting',
        'rule': 'Use reflectors and diffusers to control harsh sunlight, prioritize golden hour',
        'camera_settings': {'iso': 100, 'aperture': 2.8, 'shutter': '1/500'}
    },
    {
        'shoot_type': 'Wedding',
        'environment': 'outdoor',
        'category': 'gear',
        'rule': 'Use medium telephoto lenses (85mm, 135mm) for romantic backgrounds',
        'camera_settings': {'lenses': '85mm f/1.4, 135mm f/2'}
    },
    {
        'shoot_type': 'Wedding',
        'environment': 'outdoor',
        'category': 'composition',
        'rule': 'Frame couple with natural scenery; use leading lines from landscape',
        'camera_settings': {'aperture': 2.8, 'focus_mode': 'single_point'}
    },
    {
        'shoot_type': 'Wedding',
        'environment': 'outdoor',
        'category': 'focus',
        'rule': 'Use single-point AF for sharp focus on couple\'s eyes in bright conditions',
        'camera_settings': {'af_mode': 'single_shot', 'af_tracking': 'single_point'}
    },

    # ============== PORTRAIT ==============
    # INDOOR Portrait
    {
        'shoot_type': 'Portrait',
        'environment': 'indoor',
        'category': 'lighting',
        'rule': 'Use window light or 3-point studio lighting for flattering skin tones',
        'camera_settings': {'iso': 1600, 'aperture': 2.0, 'shutter': '1/160'}
    },
    {
        'shoot_type': 'Portrait',
        'environment': 'indoor',
        'category': 'gear',
        'rule': 'Softbox, beauty dish, or window diffuser for consistent light control',
        'camera_settings': {'light_modifier': 'softbox_60cm'}
    },
    {
        'shoot_type': 'Portrait',
        'environment': 'indoor',
        'category': 'composition',
        'rule': 'Position light at 45-degree angle for dimensional facial structure',
        'camera_settings': {'aperture': 1.8, 'focus': 'eyes'}
    },
    {
        'shoot_type': 'Portrait',
        'environment': 'indoor',
        'category': 'focus',
        'rule': 'Single AF point on eyes with back-button focus for precise control',
        'camera_settings': {'af_mode': 'single_point', 'focus_area': 'right_eye'}
    },
    # OUTDOOR Portrait
    {
        'shoot_type': 'Portrait',
        'environment': 'outdoor',
        'category': 'lighting',
        'rule': 'Use overcast days or shoot during golden hour to avoid harsh shadows',
        'camera_settings': {'iso': 400, 'aperture': 1.4, 'shutter': '1/500'}
    },
    {
        'shoot_type': 'Portrait',
        'environment': 'outdoor',
        'category': 'gear',
        'rule': 'Carry reflector for fill light and diffuser for backlit setups',
        'camera_settings': {'accessories': 'reflector_5in1, diffuser'}
    },
    {
        'shoot_type': 'Portrait',
        'environment': 'outdoor',
        'category': 'composition',
        'rule': 'Shoot into sun (backlit) with reflector fill for creamy bokeh backgrounds',
        'camera_settings': {'aperture': 1.4, 'focus': 'backlit_subject'}
    },
    {
        'shoot_type': 'Portrait',
        'environment': 'outdoor',
        'category': 'focus',
        'rule': 'Use wide aperture with zone AF to keep subject face sharp with natural background',
        'camera_settings': {'af_mode': 'zone', 'aperture': 1.4}
    },

    # ============== PRODUCT ==============
    # INDOOR Product (Studio)
    {
        'shoot_type': 'Product',
        'environment': 'indoor',
        'category': 'lighting',
        'rule': 'Use key light at 45°, fill light opposite, and back light for separation',
        'camera_settings': {'iso': 100, 'aperture': 5.6, 'shutter': '1/125'}
    },
    {
        'shoot_type': 'Product',
        'environment': 'indoor',
        'category': 'gear',
        'rule': 'Continuous LED panels or studio strobes with modifiers for controlled shadows',
        'camera_settings': {'light_type': 'studio_strobe_500w'}
    },
    {
        'shoot_type': 'Product',
        'environment': 'indoor',
        'category': 'composition',
        'rule': 'Use tripod for consistent framing; shallow depth of field to isolate product',
        'camera_settings': {'aperture': 5.6, 'focus': 'product_center'}
    },
    {
        'shoot_type': 'Product',
        'environment': 'indoor',
        'category': 'focus',
        'rule': 'Manual focus or single AF point for pixel-perfect product sharpness',
        'camera_settings': {'af_mode': 'manual', 'tripod': 'required'}
    },
    # OUTDOOR Product (Natural light)
    {
        'shoot_type': 'Product',
        'environment': 'outdoor',
        'category': 'lighting',
        'rule': 'Use diffused natural light on overcast days or in open shade for even exposure',
        'camera_settings': {'iso': 400, 'aperture': 4.0, 'shutter': '1/500'}
    },
    {
        'shoot_type': 'Product',
        'environment': 'outdoor',
        'category': 'gear',
        'rule': 'Reflectors and white foam boards to control natural light falloff',
        'camera_settings': {'accessories': 'reflector_white_board'}
    },
    {
        'shoot_type': 'Product',
        'environment': 'outdoor',
        'category': 'composition',
        'rule': 'Position product in open shade with natural background for lifestyle appeal',
        'camera_settings': {'aperture': 4.0, 'focus': 'product_detail'}
    },
    {
        'shoot_type': 'Product',
        'environment': 'outdoor',
        'category': 'focus',
        'rule': 'Use single-point AF with adequate light for accurate focus lock',
        'camera_settings': {'af_mode': 'single_point', 'af_tracking': 'off'}
    },

    # ============== LANDSCAPE ==============
    # INDOOR Landscape (City/Architecture)
    {
        'shoot_type': 'Landscape',
        'environment': 'indoor',
        'category': 'lighting',
        'rule': 'Use available ambient/architectural lighting; watch for color temperature mixed light',
        'camera_settings': {'iso': 3200, 'aperture': 2.8, 'shutter': '1/125'}
    },
    {
        'shoot_type': 'Landscape',
        'environment': 'indoor',
        'category': 'gear',
        'rule': 'Wide-angle lens (16mm, 24mm) to capture interior space context',
        'camera_settings': {'lenses': '16mm f/2.8, 24mm f/1.4'}
    },
    {
        'shoot_type': 'Landscape',
        'environment': 'indoor',
        'category': 'composition',
        'rule': 'Use leading lines (hallways, pipes) and symmetry in architectural framing',
        'camera_settings': {'aperture': 2.8, 'focus': 'hyperfocal'}
    },
    {
        'shoot_type': 'Landscape',
        'environment': 'indoor',
        'category': 'focus',
        'rule': 'Use zone AF with wide DOF to ensure entire scene sharpness',
        'camera_settings': {'af_mode': 'zone_af', 'aperture': 5.6}
    },
    # OUTDOOR Landscape (Nature)
    {
        'shoot_type': 'Landscape',
        'environment': 'outdoor',
        'category': 'lighting',
        'rule': 'Shoot during golden hour (sunrise/sunset) for warm, directional light and long shadows',
        'camera_settings': {'iso': 100, 'aperture': 8.0, 'shutter': '1/125'}
    },
    {
        'shoot_type': 'Landscape',
        'environment': 'outdoor',
        'category': 'gear',
        'rule': 'Use ND and polarizing filters; tripod for stable composition and long exposures',
        'camera_settings': {'filters': 'ND, polarizer', 'tripod': 'required'}
    },
    {
        'shoot_type': 'Landscape',
        'environment': 'outdoor',
        'category': 'composition',
        'rule': 'Apply rule of thirds; use foreground interest to create depth layering',
        'camera_settings': {'aperture': 8.0, 'focus': 'hyperfocal_distance'}
    },
    {
        'shoot_type': 'Landscape',
        'environment': 'outdoor',
        'category': 'focus',
        'rule': 'Use hyperfocal distance for maximum front-to-back sharpness from 1/3 into scene',
        'camera_settings': {'af_mode': 'manual', 'hyperfocal': 'enabled'}
    },

    # ============== SPORTS ==============
    # INDOOR Sports (Gym, Court)
    {
        'shoot_type': 'Sports',
        'environment': 'indoor',
        'category': 'lighting',
        'rule': 'Embrace gym/court ambient lighting; boost ISO to maintain fast shutter speed',
        'camera_settings': {'iso': 6400, 'aperture': 2.8, 'shutter': '1/1000'}
    },
    {
        'shoot_type': 'Sports',
        'environment': 'indoor',
        'category': 'gear',
        'rule': 'Fast telephoto lens (70-200mm f/2.8) for reach without subject disturbance',
        'camera_settings': {'lenses': '70-200mm f/2.8'}
    },
    {
        'shoot_type': 'Sports',
        'environment': 'indoor',
        'category': 'composition',
        'rule': 'Position wide to capture action in context; anticipate peak moment',
        'camera_settings': {'aperture': 2.8, 'focus_mode': 'continuous_af'}
    },
    {
        'shoot_type': 'Sports',
        'environment': 'indoor',
        'category': 'focus',
        'rule': 'Use continuous AF (AI Servo/AF-C) with wide zone for moving athletes',
        'camera_settings': {'af_mode': 'continuous', 'af_zone': 'wide', 'burst_mode': 'on'}
    },
    # OUTDOOR Sports (Field, Track)
    {
        'shoot_type': 'Sports',
        'environment': 'outdoor',
        'category': 'lighting',
        'rule': 'Daylight provides ample light; prioritize fast shutter for action freeze',
        'camera_settings': {'iso': 400, 'aperture': 4.0, 'shutter': '1/2000'}
    },
    {
        'shoot_type': 'Sports',
        'environment': 'outdoor',
        'category': 'gear',
        'rule': 'Telephoto lens (100-400mm) for distant field subjects; weather-sealed body',
        'camera_settings': {'lenses': '100-400mm f/4.5-5.6', 'weather_sealed': 'yes'}
    },
    {
        'shoot_type': 'Sports',
        'environment': 'outdoor',
        'category': 'composition',
        'rule': 'Position on sideline; capture peak action with context of field/stadium',
        'camera_settings': {'aperture': 5.6, 'focus_mode': 'continuous_af'}
    },
    {
        'shoot_type': 'Sports',
        'environment': 'outdoor',
        'category': 'focus',
        'rule': 'Burst shooting with continuous AF tracking for unpredictable action sequences',
        'camera_settings': {'af_mode': 'continuous_af', 'burst_fps': 12}
    },

    # ============== EVENT ==============
    # INDOOR Event (Party, Conference)
    {
        'shoot_type': 'Event',
        'environment': 'indoor',
        'category': 'lighting',
        'rule': 'Mix ambient and flash; use diffuser for soft fill light without harsh shadows',
        'camera_settings': {'iso': 3200, 'aperture': 2.8, 'shutter': '1/160'}
    },
    {
        'shoot_type': 'Event',
        'environment': 'indoor',
        'category': 'gear',
        'rule': 'External flash with bounce card/diffuser; wide zoom (24-70mm) for versatility',
        'camera_settings': {'flash': 'external_with_diffuser', 'lenses': '24-70mm'}
    },
    {
        'shoot_type': 'Event',
        'environment': 'indoor',
        'category': 'composition',
        'rule': 'Capture candid moments, group shots, and detail of decor/setup',
        'camera_settings': {'aperture': 2.8, 'focus': 'continuous_af'}
    },
    {
        'shoot_type': 'Event',
        'environment': 'indoor',
        'category': 'focus',
        'rule': 'Use zone AF or wide-area AF to track moving people during indoor events',
        'camera_settings': {'af_mode': 'zone_af', 'af_area': 'wide'}
    },
    # OUTDOOR Event (Wedding Reception, Festival)
    {
        'shoot_type': 'Event',
        'environment': 'outdoor',
        'category': 'lighting',
        'rule': 'Use natural light when possible; bring flash for fill light at twilight',
        'camera_settings': {'iso': 800, 'aperture': 2.8, 'shutter': '1/500'}
    },
    {
        'shoot_type': 'Event',
        'environment': 'outdoor',
        'category': 'gear',
        'rule': 'Versatile zoom (35-85mm equivalent) for close-ups and wide group shots',
        'camera_settings': {'lenses': '35-85mm'}
    },
    {
        'shoot_type': 'Event',
        'environment': 'outdoor',
        'category': 'composition',
        'rule': 'Frame activities with outdoor scenery; capture atmosphere and interaction',
        'camera_settings': {'aperture': 2.8, 'focus': 'continuous_af'}
    },
    {
        'shoot_type': 'Event',
        'environment': 'outdoor',
        'category': 'focus',
        'rule': 'Continuous AF with subject tracking for dynamic outdoor event coverage',
        'camera_settings': {'af_mode': 'continuous', 'af_tracking': 'subject_tracking'}
    },

    # ============== FASHION ==============
    # INDOOR Fashion (Studio)
    {
        'shoot_type': 'Fashion',
        'environment': 'indoor',
        'category': 'lighting',
        'rule': 'Use key light + fill + backdrop light for magazine-quality separation',
        'camera_settings': {'iso': 100, 'aperture': 5.6, 'shutter': '1/160'}
    },
    {
        'shoot_type': 'Fashion',
        'environment': 'indoor',
        'category': 'gear',
        'rule': 'Medium telephoto (70-85mm) for flattering facial proportions; studio strobes',
        'camera_settings': {'lenses': '85mm f/1.8', 'light': 'studio_strobe'}
    },
    {
        'shoot_type': 'Fashion',
        'environment': 'indoor',
        'category': 'composition',
        'rule': 'Full-body and detail shots; emphasize garment texture and silhouette',
        'camera_settings': {'aperture': 5.6, 'focus': 'manual'}
    },
    {
        'shoot_type': 'Fashion',
        'environment': 'indoor',
        'category': 'focus',
        'rule': 'Manual focus for precise control; ensure model\'s eyes/face is sharp',
        'camera_settings': {'af_mode': 'manual', 'focus_area': 'model_face'}
    },
    # OUTDOOR Fashion (Location)
    {
        'shoot_type': 'Fashion',
        'environment': 'outdoor',
        'category': 'lighting',
        'rule': 'Golden hour backlit for rim light; use reflector for face fill',
        'camera_settings': {'iso': 400, 'aperture': 2.8, 'shutter': '1/500'}
    },
    {
        'shoot_type': 'Fashion',
        'environment': 'outdoor',
        'category': 'gear',
        'rule': 'Medium zoom (50-85mm) + reflector for portable, location-based shooting',
        'camera_settings': {'lenses': '50-85mm', 'accessories': 'reflector_5in1'}
    },
    {
        'shoot_type': 'Fashion',
        'environment': 'outdoor',
        'category': 'composition',
        'rule': 'Use environmental backdrop; dynamic posing with model interaction',
        'camera_settings': {'aperture': 2.8, 'focus': 'continuous_af'}
    },
    {
        'shoot_type': 'Fashion',
        'environment': 'outdoor',
        'category': 'focus',
        'rule': 'Single-point AF on model\'s eyes; use continuous mode for posed movement',
        'camera_settings': {'af_mode': 'single_point', 'focus_area': 'eyes'}
    }
]

# Insert rules into MongoDB
try:
    result = lighting_rules_collection.insert_many(rules)
    print(f"✓ Inserted {len(result.inserted_ids)} environment-specific lighting rules")
    print(f"  Rules include indoor/outdoor variants for all 7 shoot types")
except Exception as e:
    print(f"✗ Failed to insert rules: {e}")
    exit(1)

# Verify by showing counts
for shoot_type in ['Wedding', 'Portrait', 'Product', 'Landscape', 'Sports', 'Event', 'Fashion']:
    indoor_count = lighting_rules_collection.count_documents({'shoot_type': shoot_type, 'environment': 'indoor'})
    outdoor_count = lighting_rules_collection.count_documents({'shoot_type': shoot_type, 'environment': 'outdoor'})
    print(f"  {shoot_type}: {indoor_count} indoor + {outdoor_count} outdoor = {indoor_count + outdoor_count} total")

print("\n✓ Environment-specific lighting rules seeded successfully!")
