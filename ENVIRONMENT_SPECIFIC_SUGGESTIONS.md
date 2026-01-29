# Environment-Specific Lighting Suggestions Guide

## Overview
The chatbot now provides **differentiated lighting and camera settings** based on whether you're shooting **indoors** or **outdoors** for each shoot type.

## How It Works

### 1. Database Structure
- **56 lighting rules** seeded into MongoDB (7 shoot types × 8 rules each)
- Each rule has an `environment` field: either `"indoor"` or `"outdoor"`
- Rules include: lighting setup, gear recommendations, composition tips, and camera settings

### 2. Backend `/api/chat` Endpoint
The chatbot now accepts:
```json
{
  "message": "What lighting should I use?",
  "shoot_type": "Wedding",
  "environment": "indoor"  // NEW!
}
```

**Query Logic:**
- Fetches rules where `shoot_type = "Wedding"` AND `environment = "indoor"`
- Returns only suggestions suitable for indoor wedding photography
- Includes camera settings: ISO, aperture, shutter speed, recommended lenses, etc.

### 3. Frontend Integration
The environment is set by:
- **Dashboard:** When user clicks "Indoor Shoot" or "Outdoor Shoot", it saves to `localStorage.selectedCategory`
- **Chatbot:** Reads the environment from localStorage and sends it with each message

## Example Workflow

### Scenario: Wedding Photography

**Step 1: User is on Dashboard**
```
Dashboard shows: Wedding (with Indoor/Outdoor buttons)
User clicks: "Indoor Shoot"
```

**Step 2: User navigates to Workspace/Chatbot**
```
localStorage.selectedCategory = "indoor"
localStorage.selectedShootType = "Wedding"
```

**Step 3: User asks Chatbot**
```
User: "What lighting setup should I use?"
Sent to /api/chat:
{
  "message": "What lighting setup should I use?",
  "shoot_type": "Wedding",
  "environment": "indoor"
}
```

**Step 4: Chatbot Returns Indoor-Specific Response**
```
Response:
"Use soft, diffused light with minimal harsh shadows for elegant indoor ceremonies.
Recommended Settings: iso: 3200, aperture: 1.4, shutter: 1/250"
```

---

## Environment-Specific Rules by Shoot Type

### Wedding
**Indoor:**
- Soft, diffused light with minimal shadows
- Fast primes: 24mm f/1.4, 35mm f/1.4, 50mm f/1.4
- ISO: 3200, f/1.4, 1/250
- Continuous AF for moving subjects

**Outdoor:**
- Golden hour, reflectors & diffusers for sun control
- Telephoto: 85mm f/1.4, 135mm f/2
- ISO: 100, f/2.8, 1/500
- Single-point AF for sharp eye focus

### Portrait
**Indoor:**
- Window light or 3-point studio lighting
- Softbox, beauty dish, or diffuser
- ISO: 1600, f/2.0, 1/160
- 45-degree light angle for facial structure

**Outdoor:**
- Overcast days or golden hour
- Use reflectors and backlighting
- ISO: 400, f/1.4, 1/500
- Creamy bokeh with wide aperture

### Product
**Indoor:**
- 3-point studio lighting (key, fill, back)
- Studio strobes or continuous LED panels
- ISO: 100, f/5.6, 1/125
- Manual focus for precision

**Outdoor:**
- Diffused natural light / open shade
- White reflectors and foam boards
- ISO: 400, f/4.0, 1/500
- Even exposure without harsh shadows

### Landscape
**Indoor:**
- Ambient/architectural lighting
- Wide-angle lenses: 16mm, 24mm
- ISO: 3200, f/2.8, 1/125
- Leading lines and symmetry in framing

**Outdoor:**
- Golden hour with long shadows
- ND & polarizing filters, tripod required
- ISO: 100, f/8.0, 1/125
- Hyperfocal distance for max sharpness

### Sports
**Indoor:**
- Embrace gym/court ambient lighting
- Fast telephoto: 70-200mm f/2.8
- ISO: 6400, f/2.8, 1/1000
- Continuous AF with burst mode

**Outdoor:**
- Daylight provides ample light
- Telephoto: 100-400mm f/4.5-5.6
- ISO: 400, f/4.0, 1/2000
- Burst shooting for action sequences

### Event
**Indoor:**
- Mix ambient + flash with diffuser
- External flash + wide zoom: 24-70mm
- ISO: 3200, f/2.8, 1/160
- Zone AF for moving people

**Outdoor:**
- Natural light + flash for fill at twilight
- Versatile zoom: 35-85mm
- ISO: 800, f/2.8, 1/500
- Subject tracking for dynamic coverage

### Fashion
**Indoor:**
- Key + fill + backdrop lighting
- Medium telephoto: 85mm f/1.8
- Studio strobes
- ISO: 100, f/5.6, 1/160
- Manual focus for control

**Outdoor:**
- Golden hour backlit with reflector fill
- Medium zoom: 50-85mm + reflector
- ISO: 400, f/2.8, 1/500
- Single-point AF on model's eyes

---

## Testing the Feature

### Test Case 1: Indoor Wedding
1. Login to app
2. Go to Dashboard
3. Click "Wedding" → "Indoor Shoot"
4. Ask chatbot: "What lighting should I use?"
5. ✅ Should receive **indoor wedding** lighting tips (soft light, high ISO, f/1.4)

### Test Case 2: Outdoor Wedding
1. Go back to Dashboard
2. Click "Wedding" → "Outdoor Shoot"
3. Ask same question
4. ✅ Should receive **outdoor wedding** lighting tips (golden hour, reflectors, lower ISO, f/2.8)

### Test Case 3: Indoor Portrait
1. Dashboard → "Portrait" → "Indoor Shoot"
2. Ask: "What camera settings?"
3. ✅ Should show **studio portrait** settings (ISO 1600, f/2.0, softbox setup)

### Test Case 4: Outdoor Portrait
1. Dashboard → "Portrait" → "Outdoor Shoot"
2. Ask same question
3. ✅ Should show **outdoor portrait** settings (ISO 400, f/1.4, reflectors, golden hour)

---

## Database Query Examples

### Query: Lighting rules for Indoor Wedding Photography
```javascript
db.lighting_rules.find({
  shoot_type: "Wedding",
  environment: "indoor"
})
// Returns 4 rules for different aspects: lighting, gear, composition, focus
```

### Query: All environments for Sports
```javascript
db.lighting_rules.find({
  shoot_type: "Sports"
})
// Returns 8 rules: 4 indoor gym, 4 outdoor field
```

---

## Files Modified

1. **`seed_lighting_rules_with_env.py`** (NEW)
   - Creates 56 environment-specific lighting rules
   - Run once to populate MongoDB

2. **`app.py`**
   - Updated `/api/chat` to accept `environment` parameter
   - Added filtering by both `shoot_type` AND `environment`
   - Improved logging with environment info

3. **`static/script.js`**
   - Updated `sendChatMessage()` to read `selectedCategory` from localStorage
   - Sends `environment` field to `/api/chat`

4. **MongoDB `lighting_rules` collection**
   - Added `environment` field (string: "indoor" or "outdoor")
   - Each rule now has metadata for specific environments

---

## Future Enhancements

- [ ] Add time-of-day specific suggestions (golden hour, midday, night)
- [ ] Add weather-based suggestions (cloudy, clear, rain)
- [ ] Add location presets (studio, park, beach, mountains)
- [ ] Create visual pose variations by environment
- [ ] Track which environment settings produce best results

---

## Support

If the chatbot is not returning differentiated suggestions:
1. Check Flask logs for `[CHAT]` messages
2. Verify `selectedCategory` is in localStorage (DevTools → Application → Local Storage)
3. Run `python seed_lighting_rules_with_env.py` again to ensure rules are in DB
4. Restart Flask server

