# Quick Start Guide: Photo Analysis Storage

## 🚀 In 5 Minutes

### What was added?
When a photographer analyzes a scene in the camera UI, the photo is automatically stored in their profile and MongoDB.

---

## ⚙️ Setup

### 1. Install Required Package
```bash
pip install Pillow
```

### 2. Start MongoDB
```bash
mongod
```

### 3. Start Flask App
```bash
python app.py
```

---

## 📸 How to Use

### As a User:
1. **Log in** to the application
2. **Go to Dashboard** → click **"AI Scene Analyzer"**
3. **Click "Start Camera"** or **"Upload Image"**
4. **Capture photo** or select image file
5. **Click "Capture & Analyze"**
6. ✅ See message: **"Photo successfully analyzed and saved to your profile!"**
7. Photo is now:
   - 💾 Saved in file system (`static/uploads/`)
   - 🗄️ Stored in MongoDB
   - 👤 Linked to your profile

---

## 🔄 What Happens Behind the Scenes

```
You click "Capture & Analyze"
         ↓
JavaScript sends image to server
         ↓
Server decodes image
         ↓
Server saves to static/uploads/
         ↓
Server stores in MongoDB analyzed_photos
         ↓
Server updates your profile
         ↓
You see success message
```

---

## 📁 Files Changed

| File | What Changed |
|------|-------------|
| `app.py` | Added 3 new API endpoints + MongoDB collection |
| `camera.html` | No changes (already compatible) |

---

## 💾 Where Data is Stored

### Files
- **Location:** `static/uploads/`
- **Format:** `analyzed_photo_{user_id}_{timestamp}.jpg`
- **Example:** `analyzed_photo_507f1f77bcf86cd799439011_20260122_143022.jpg`

### Database
- **Collection:** `analyzed_photos` (new)
- **Database:** `photomind` (existing)
- **Stored:** Image path, filename, timestamp, user ID

### Your Profile
- **Field:** `photographers.analyzed_photos`
- **Contains:** Reference to each analyzed photo

---

## 🔍 View Your Photos

### Via API (Browser Console)
```javascript
fetch('/api/analyzed-photos')
  .then(res => res.json())
  .then(data => console.log(data.analyzed_photos))
```

### Via MongoDB
```bash
mongosh
use photomind
db.analyzed_photos.find()
```

---

## 🗑️ Delete a Photo

### Via API (Browser Console)
```javascript
fetch('/api/analyzed-photos/PHOTO_ID_HERE', {
  method: 'DELETE'
})
.then(res => res.json())
.then(data => console.log(data.message))
```

Deletes from:
- 📁 File system
- 🗄️ MongoDB
- 👤 Your profile

---

## 🧪 Testing Checklist

- [ ] MongoDB is running
- [ ] Flask app is running
- [ ] You are logged in
- [ ] Camera UI loads correctly
- [ ] Photo capture works
- [ ] You see "Photo successfully analyzed..." message
- [ ] File appears in `static/uploads/`
- [ ] Document appears in MongoDB `analyzed_photos` collection
- [ ] `/api/analyzed-photos` returns your photos
- [ ] Can delete photos successfully

---

## 📊 New API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/analyze-scene` | Analyze & store photo |
| GET | `/api/analyzed-photos` | Retrieve your photos |
| DELETE | `/api/analyzed-photos/{id}` | Delete a photo |

---

## 🆘 Troubleshooting

### Problem: "Unauthorized" Error
- **Cause:** Not logged in
- **Fix:** Log in first

### Problem: Photo not saving
- **Cause:** Missing Pillow library
- **Fix:** `pip install Pillow`

### Problem: MongoDB error
- **Cause:** MongoDB not running
- **Fix:** Start MongoDB: `mongod`

### Problem: File not appearing in uploads
- **Cause:** Permission issue or directory missing
- **Fix:** Ensure `static/uploads/` exists and is writable

### Problem: No photos in API response
- **Cause:** No photos analyzed yet OR not logged in as same user
- **Fix:** Analyze a photo first, ensure you're logged in

---

## 📝 Documentation Files

| File | Content |
|------|---------|
| `PHOTO_STORAGE_SUMMARY.md` | Overview & diagrams |
| `PHOTO_STORAGE_IMPLEMENTATION.md` | Technical details |
| `API_DOCUMENTATION.md` | Full API reference |
| `IMPLEMENTATION_CHECKLIST.md` | What was done |

---

## ✨ Key Features

✅ **Auto-Save** - Photos saved when you analyze  
✅ **Always Accessible** - View via API anytime  
✅ **Easy Delete** - Remove unwanted photos  
✅ **Permanent Storage** - Photos never lost (unless deleted)  
✅ **User-Isolated** - Can only see own photos  
✅ **Timestamp Tracked** - Know when each was analyzed  

---

## 🎯 Next Steps

1. ✅ Feature is complete and ready to use
2. 🧪 Test it with your camera
3. 📖 Read detailed docs if needed
4. 🚀 Deploy when ready

---

## 💡 Tips

- Photos are stored with your user ID to keep them private
- Each photo gets a unique timestamp filename
- You can safely delete photos - files are removed too
- Photos are backed up in MongoDB for reliability
- Check `static/uploads/` folder to see files on disk

---

## 🎉 You're All Set!

Your photo analysis feature is ready. Start the app and try it out!

```bash
python app.py
# Visit http://localhost:5000
# Log in → Dashboard → AI Scene Analyzer → Capture Photo
```

Enjoy! 📸✨
