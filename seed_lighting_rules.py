"""
Seed script to populate lighting rules and camera settings for each shoot type.
Run this once to populate the MongoDB database with comprehensive lighting and settings data.
"""

from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['photomind']
lighting_rules_collection = db['lighting_rules']
shoot_types_collection = db['shoot_types']

# Lighting and settings data by shoot type
lighting_data = {
    'Wedding': [
        {
            'shoot_type': 'Wedding',
            'category': 'lighting',
            'rule': 'Golden Hour Light: Schedule portraits during golden hour (1 hour before sunset) for warm, flattering skin tones and romantic atmosphere.',
            'settings': {'iso': '100-400', 'aperture': 'f/2.0-f/2.8', 'shutter': '1/250s'}
        },
        {
            'shoot_type': 'Wedding',
            'category': 'lighting',
            'rule': 'Ceremony Lighting: Use available light (window light, candles). Increase ISO to 1600-3200 if needed. Avoid flash on altar.',
            'settings': {'iso': '1600-3200', 'aperture': 'f/2.8-f/4.0', 'shutter': '1/125s'}
        },
        {
            'shoot_type': 'Wedding',
            'category': 'lighting',
            'rule': 'Reception Lighting: Bounce flash off ceiling for even lighting. Use high ISO (3200+) and fast aperture (f/2.0) for dancing scenes.',
            'settings': {'iso': '3200-6400', 'aperture': 'f/1.8-f/2.8', 'shutter': '1/125s'}
        },
        {
            'shoot_type': 'Wedding',
            'category': 'gear',
            'rule': 'Backup Gear: Always bring 2 camera bodies, 3 lenses (24-70mm, 70-200mm, 35mm), extra batteries, and SD cards.',
            'settings': {'lenses': ['24-70mm', '70-200mm', '35mm f/1.8'], 'batteries': '3+', 'cards': '64GB+'}
        },
        {
            'shoot_type': 'Wedding',
            'category': 'composition',
            'rule': 'Emotion Capture: Focus on genuine moments - first kiss, parent reactions, dancing joy. Use burst mode for decisive moments.',
            'settings': {'mode': 'burst', 'focus': 'continuous-af', 'metering': 'matrix'}
        }
    ],
    'Portrait': [
        {
            'shoot_type': 'Portrait',
            'category': 'lighting',
            'rule': 'Three-Point Lighting: Key light at 45°, fill light opposite, backlight for separation. Creates depth and dimension.',
            'settings': {'iso': '100-400', 'aperture': 'f/2.0-f/4.0', 'shutter': '1/250s'}
        },
        {
            'shoot_type': 'Portrait',
            'category': 'lighting',
            'rule': 'Window Light: Position subject perpendicular to window. Use white reflector on shadow side. Soft, natural, flattering.',
            'settings': {'iso': '200-800', 'aperture': 'f/2.8-f/5.6', 'shutter': '1/125s'}
        },
        {
            'shoot_type': 'Portrait',
            'category': 'gear',
            'rule': 'Portrait Lenses: 50mm f/1.8 (standard), 85mm f/1.4 (professional), 35mm f/2.0 (environmental portraits).',
            'settings': {'lenses': ['50mm f/1.8', '85mm f/1.4', '35mm f/2.0']}
        },
        {
            'shoot_type': 'Portrait',
            'category': 'composition',
            'rule': 'Focus on Eyes: Eyes must be tack sharp. Use single AF point, focus on nearest eye. Shallow DOF (f/2.0-f/4.0).',
            'settings': {'focus': 'single-af', 'metering': 'spot', 'dof': 'f/2.0-f/4.0'}
        }
    ],
    'Event': [
        {
            'shoot_type': 'Event',
            'category': 'lighting',
            'rule': 'Ambient Light Priority: Preserve venue atmosphere. Use high ISO (1600-3200) and fast lenses. Minimize flash when possible.',
            'settings': {'iso': '1600-3200', 'aperture': 'f/2.0-f/2.8', 'shutter': '1/125s'}
        },
        {
            'shoot_type': 'Event',
            'category': 'lighting',
            'rule': 'Flash Technique: Bounce flash for even coverage. TTL mode for consistency. Use diffuser to soften light.',
            'settings': {'iso': '800-1600', 'aperture': 'f/2.8-f/4.0', 'shutter': '1/125s', 'flash': 'TTL-bounce'}
        },
        {
            'shoot_type': 'Event',
            'category': 'gear',
            'rule': 'Event Kit: Wide zoom (24-70mm), telephoto (70-200mm), fast prime (35mm f/1.8), external flash, extra batteries.',
            'settings': {'lenses': ['24-70mm', '70-200mm', '35mm f/1.8'], 'flash': 'external TTL', 'batteries': '4+'}
        }
    ],
    'Product': [
        {
            'shoot_type': 'Product',
            'category': 'lighting',
            'rule': 'Continuous Lighting: Use softboxes or light tents for consistent, shadow-free lighting. 5500K daylight balance.',
            'settings': {'iso': '100-400', 'aperture': 'f/8-f/16', 'shutter': '1/125s', 'wb': '5500K'}
        },
        {
            'shoot_type': 'Product',
            'category': 'lighting',
            'rule': 'Backlighting: Place light behind product for edge highlights. Use reflector to fill shadows. Creates premium look.',
            'settings': {'iso': '200-400', 'aperture': 'f/11-f/16', 'shutter': '1/250s'}
        },
        {
            'shoot_type': 'Product',
            'category': 'composition',
            'rule': 'Background: Use plain white, grey, or themed backgrounds. Ensure sharp focus across entire product (high aperture).',
            'settings': {'focus': 'manual-focus', 'aperture': 'f/11-f/22', 'metering': 'spot'}
        },
        {
            'shoot_type': 'Product',
            'category': 'gear',
            'rule': 'Product Setup: Macro lens (90-100mm), ring light or softbox, light tent, tripod (essential), white/black reflectors.',
            'settings': {'lenses': ['90mm macro', '50mm'], 'lighting': 'ring-light or softbox'}
        }
    ],
    'Landscape': [
        {
            'shoot_type': 'Landscape',
            'category': 'lighting',
            'rule': 'Golden Hour: Shoot within 1 hour of sunrise/sunset. Low angle light creates dramatic shadows and warm colors.',
            'settings': {'iso': '50-200', 'aperture': 'f/8-f/16', 'shutter': '1/60-1/250s'}
        },
        {
            'shoot_type': 'Landscape',
            'category': 'lighting',
            'rule': 'Blue Hour: Twilight after sunset (20-40 min). Deep blue sky, balanced artificial lights. ISO 400-1600, tripod essential.',
            'settings': {'iso': '400-1600', 'aperture': 'f/4-f/8', 'shutter': '1-10s', 'tripod': 'required'}
        },
        {
            'shoot_type': 'Landscape',
            'category': 'composition',
            'rule': 'Depth Layers: Foreground (interesting element), midground (subject), background (sky). Use leading lines, rule of thirds.',
            'settings': {'composition': 'leading-lines', 'rule': 'thirds', 'focus': 'hyperfocal'}
        },
        {
            'shoot_type': 'Landscape',
            'category': 'gear',
            'rule': 'Landscape Essentials: Wide angle (16-35mm), sturdy tripod, ND and polarizing filters, extra batteries (long exposures drain them).',
            'settings': {'lenses': ['16-35mm', '24-70mm'], 'filters': ['ND', 'CPL'], 'tripod': 'required'}
        }
    ],
    'Fashion': [
        {
            'shoot_type': 'Fashion',
            'category': 'lighting',
            'rule': 'Studio Lighting: 3-light setup with key, fill, and backlight. Softboxes for flattering light. Shadows define shape.',
            'settings': {'iso': '100-400', 'aperture': 'f/4-f/8', 'shutter': '1/250s', 'flash': 'studio'}
        },
        {
            'shoot_type': 'Fashion',
            'category': 'lighting',
            'rule': 'Outdoor Fashion: Position model with sun at 45° angle (not directly behind). Use reflector to fill facial shadows.',
            'settings': {'iso': '100-200', 'aperture': 'f/2.8-f/5.6', 'shutter': '1/500-1/1000s'}
        },
        {
            'shoot_type': 'Fashion',
            'category': 'gear',
            'rule': 'Fashion Lenses: 50mm f/1.8 (versatile), 70-200mm (flattering compression), 35mm f/2.0 (full body shots).',
            'settings': {'lenses': ['50mm f/1.8', '70-200mm', '35mm f/2.0']}
        },
        {
            'shoot_type': 'Fashion',
            'category': 'composition',
            'rule': 'Model Direction: Create angles with body (S-curve), elongate limbs, tilt head slightly. Natural, confident postures.',
            'settings': {'pose': 's-curve', 'posture': 'confident', 'angles': 'varied'}
        }
    ],
    'Sports': [
        {
            'shoot_type': 'Sports',
            'category': 'lighting',
            'rule': 'Continuous Action: High shutter speed (1/1000s+), fast ISO (1600-3200), fast aperture (f/2.8-f/4.0). Freeze motion.',
            'settings': {'iso': '1600-3200', 'aperture': 'f/2.8-f/4.0', 'shutter': '1/1000s+'}
        },
        {
            'shoot_type': 'Sports',
            'category': 'lighting',
            'rule': 'Backlit Subjects: Avoid shooting into harsh sunlight. Underexpose slightly, then recover in post. Adds drama.',
            'settings': {'iso': '800-1600', 'aperture': 'f/4-f/5.6', 'shutter': '1/500-1/1000s', 'exposure': '-0.5 to -1 EV'}
        },
        {
            'shoot_type': 'Sports',
            'category': 'gear',
            'rule': 'Sports Kit: Fast telephoto (70-200mm f/2.8), secondary body with wide lens, burst mode (10+ fps), extra batteries.',
            'settings': {'lenses': ['70-200mm f/2.8'], 'fps': '10+', 'bodies': '2', 'batteries': '4+'}
        },
        {
            'shoot_type': 'Sports',
            'category': 'focus',
            'rule': 'Continuous AF: Use AI Servo (Canon) or AF-C (Sony/Nikon). Track subjects. Prefocus on action zones.',
            'settings': {'focus': 'continuous-af', 'tracking': 'enabled', 'fps': 'max'}
        }
    ]
}

def seed_lighting_rules():
    """Populate lighting rules into MongoDB."""
    print("Starting to seed lighting rules...")
    
    for shoot_type, rules in lighting_data.items():
        print(f"\n--- {shoot_type} ---")
        for rule_data in rules:
            try:
                # Check if rule already exists (to avoid duplicates)
                existing = lighting_rules_collection.find_one({
                    'shoot_type': rule_data['shoot_type'],
                    'rule': rule_data['rule']
                })
                
                if not existing:
                    rule_data['created_at'] = datetime.now()
                    result = lighting_rules_collection.insert_one(rule_data)
                    print(f"  ✓ Added: {rule_data['category']} - {rule_data['rule'][:60]}...")
                else:
                    print(f"  - Skipped (exists): {rule_data['category']} - {rule_data['rule'][:60]}...")
            except Exception as e:
                print(f"  ✗ Error: {e}")
    
    print("\n✓ Lighting rules seeding complete!")

if __name__ == '__main__':
    seed_lighting_rules()
