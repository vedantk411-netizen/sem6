# Chatbot Lighting & Settings Enhancement

## Summary
Enhanced the AI Photography Chatbot to dynamically fetch and serve comprehensive lighting rules, camera settings, and gear recommendations for each photography shoot type.

## Changes Made

### 1. **Comprehensive Seed Data** (`seed_lighting_rules.py`)
- Created structured lighting and settings database with 27 rules across 7 shoot types
- Categories: `lighting`, `gear`, `composition`, `focus`
- Each rule includes recommended camera settings (ISO, aperture, shutter speed, etc.)

**Shoot Types Covered:**
- **Wedding**: Golden hour, ceremony lighting, reception lighting, backup gear, emotion capture
- **Portrait**: Three-point lighting, window light, portrait lenses, focus on eyes
- **Event**: Ambient light priority, flash technique, event kit essentials
- **Product**: Continuous lighting, backlighting, background setup, macro equipment
- **Landscape**: Golden hour, blue hour, depth layers, tripod essentials
- **Fashion**: Studio lighting, outdoor fashion, fashion lenses, model direction
- **Sports**: Continuous action, backlit subjects, sports equipment, continuous AF

### 2. **Backend Chatbot Upgrade** (`app.py`)
Enhanced `/api/chat` endpoint with dynamic MongoDB fetching:

```javascript
POST /api/chat
{
  "message": "What lighting for wedding?",
  "shoot_type": "Wedding"  // Optional filter
}
```

**Features:**
- Detects shoot types from user messages automatically
- Fetches matching rules based on keyword categories (lighting, gear, composition, focus)
- Returns formatted response with recommended settings (ISO, aperture, shutter speed, etc.)
- Falls back to keyword matching if no DB rules match
- Logs all chats with shoot type for analytics

### 3. **Chatbot UI Enhancement** (`templates/chatbot.html`)
Added shoot type selector dropdown:
- All Types (default)
- Wedding
- Portrait
- Product
- Landscape
- Event
- Fashion
- Sports

### 4. **Frontend Integration** (`static/script.js`)
Updated chat sending logic to include selected shoot type in API payload for targeted recommendations.

## Example Interactions

### Example 1: Generic Lighting Question
```
User: "What lighting should I use?"
Chatbot: "Three-Point Lighting: Key light at 45°, fill light opposite, backlight for separation. Creates depth and dimension. Recommended Settings: iso: 100-400, aperture: f/2.0-f/4.0, shutter: 1/250s"
```

### Example 2: Shoot Type Filtered Question
```
User: Selects "Wedding" from dropdown
User: "Tell me about the reception"
Chatbot: "Reception Lighting: Bounce flash off ceiling for even lighting. Use high ISO (3200+) and fast aperture (f/2.0) for dancing scenes. Recommended Settings: iso: 3200-6400, aperture: f/1.8-f/2.8, shutter: 1/125s"
```

### Example 3: Gear Recommendations
```
User: Selects "Sports"
User: "What equipment do I need?"
Chatbot: "Sports Kit: Fast telephoto (70-200mm f/2.8), secondary body with wide lens, burst mode (10+ fps), extra batteries. Recommended Settings: lenses: 70-200mm f/2.8, fps: 10+, bodies: 2, batteries: 4+"
```

## Database Schema

### lighting_rules collection
```javascript
{
  "shoot_type": "Wedding",
  "category": "lighting",
  "rule": "Golden Hour Light: Schedule portraits during golden hour...",
  "settings": {
    "iso": "100-400",
    "aperture": "f/2.0-f/2.8",
    "shutter": "1/250s"
  },
  "created_at": "2026-01-29T..."
}
```

## How to Use

### 1. Populate Database
```bash
python seed_lighting_rules.py
```

### 2. Chat with Filtered Type
- Visit `/chatbot`
- Select shoot type from dropdown (or leave as "All Types")
- Ask questions like:
  - "What lighting should I use?"
  - "What equipment do I need?"
  - "How do I focus?"
  - "Tell me about poses"

### 3. Smart Detection
- Type "wedding lighting" and the chatbot auto-detects "Wedding"
- Ask "What's the gear for product photography?" and get product-specific rules

## Benefits

✅ **Comprehensive Knowledge Base** - 27+ professional photography rules in database  
✅ **Dynamic Responses** - Fetches from MongoDB instead of hardcoded keywords  
✅ **Shoot Type Filtering** - Get targeted advice for specific photography types  
✅ **Professional Settings** - Every tip includes recommended ISO, aperture, shutter speed  
✅ **Extensible** - Add more rules to MongoDB without code changes  
✅ **Analytics** - Track user questions and shoot type preferences  

## Testing

### Test Coverage
- Generic questions without shoot type
- Questions with auto-detected shoot types
- Filtered questions with selected shoot type
- Edge cases (empty messages, invalid shoot types)

### Terminal Commands
```bash
# Seed the data
python seed_lighting_rules.py

# Count loaded rules
# MongoDB: db.lighting_rules.countDocuments()
# Expected: 27+ rules
```

## Future Enhancements

- Add user preferences to AI model (remember favorite settings)
- ML-based recommendation engine (similar questions, similar answers)
- Video tutorials linked to lighting rules
- Community tips and user-submitted rules
- Advanced filters (gear brand, budget, experience level)
