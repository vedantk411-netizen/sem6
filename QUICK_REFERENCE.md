# Quick Reference Guide - New Features

## 🎯 Quick Start

### For Users (Photographers)

1. **Register with Preferences**
   - Click "Create Account" on home page
   - Fill: Name, Email, Password
   - Optional: Select Experience Level, Specialization, Equipment
   - Click "Sign Up"

2. **Send Message to Admin**
   - From dashboard, click orange "Send Message" button
   - Enter Subject and Message
   - Click "Send Message"

3. **Check Shoot History** (API)
   - GET /api/shoot-history
   - Returns all your past shoots

### For Admins

1. **View Chat Requests**
   - Login as admin
   - Click "Chat Requests" tab
   - See all photographer messages

2. **Respond to Messages**
   - Click "Respond" button
   - Type response in prompt
   - Message status updates to "Responded"

3. **Filter Messages**
   - Click status buttons: All, New, Read, Responded

---

## 📊 Data Models

### Photographer Preferences
```javascript
{
  specialization: ["Wedding", "Portrait"],
  experience_level: "intermediate",
  equipment: ["Canon", "Sony"]
}
```

### Shoot History Entry
```javascript
{
  shoot_type: "Wedding",
  location: "Central Park",
  notes: "Beautiful sunset",
  images_count: 250,
  date: "2026-01-21T..."
}
```

### Chat Request
```javascript
{
  subject: "Help with lighting",
  message: "How do I setup studio lighting?",
  status: "new",  // can be: new, read, responded, closed
  response: "Use 3-point lighting..."
}
```

---

## 🔌 API Quick Reference

### Authentication
All endpoints need user to be logged in (session required)

### User Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/preferences` | Get your preferences |
| PUT | `/api/preferences` | Update your preferences |
| GET | `/api/shoot-history` | Get your shoots |
| POST | `/api/shoot-history` | Add a shoot |
| POST | `/api/chat-requests` | Send message to admin |

### Admin Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/chat-requests?status=new` | Get messages |
| PUT | `/api/chat-requests/{id}` | Respond to message |
| DELETE | `/api/chat-requests/{id}` | Delete message |

---

## 🛠️ Code Snippets

### Send Message (JavaScript)
```javascript
fetch('/api/chat-requests', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    subject: 'Help needed',
    message: 'How do I...?'
  })
}).then(res => res.json())
  .then(data => console.log(data.message))
```

### Get Preferences (JavaScript)
```javascript
fetch('/api/preferences')
  .then(res => res.json())
  .then(prefs => console.log(prefs.specialization))
```

### Update Preferences (JavaScript)
```javascript
fetch('/api/preferences', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    specialization: ['Wedding', 'Portrait'],
    experience_level: 'expert',
    equipment: ['Canon', 'Nikon']
  })
}).then(res => res.json())
```

### Log a Shoot (JavaScript)
```javascript
fetch('/api/shoot-history', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    shoot_type: 'Wedding',
    location: 'Hotel Grand',
    notes: 'Perfect weather',
    images_count: 500
  })
}).then(res => res.json())
```

### Admin Responds (JavaScript)
```javascript
fetch('/api/chat-requests/REQUEST_ID', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    status: 'responded',
    response: 'Here is my response...'
  })
}).then(res => res.json())
```

---

## 🎨 UI Components Added

### Registration Form
- Added preferences section below password field
- Experience Level dropdown
- Specialization checkboxes (5 options)
- Equipment checkboxes (5 options)

### Dashboard Navbar
- New orange "Send Message" button
- Opens modal for composing messages

### Chat Modal
- Subject field
- Message textarea
- Send and Cancel buttons
- Closes on ESC or outside click

### Admin Dashboard
- New "Chat Requests" tab
- Status filter buttons
- Message cards with details
- Action buttons (Mark Read, Respond, Delete)
- Response display section

---

## 🗄️ MongoDB Collections

All collections are auto-created on first run:

```
photographer_preferences  - User specialization, experience, equipment
shoot_history            - User's shooting sessions log
chat_requests            - Messages from users to admin
```

---

## 🔐 Security Features

✅ Session-based authentication
✅ Password hashing (bcrypt)
✅ User data isolation
✅ Admin-only operations
✅ Input validation
✅ ObjectId validation

---

## 📝 Form Fields Reference

### Registration Preferences
- **Experience Level** (dropdown): beginner, intermediate, expert
- **Specialization** (checkboxes): Wedding, Portrait, Event, Outdoor, Product
- **Equipment** (checkboxes): Canon, Nikon, Sony, GoPro, DJI Drones

### Chat Request Form
- **Subject** (text): Brief topic (max 100 chars recommended)
- **Message** (textarea): Detailed message (no limit)

### Shoot History
- **Shoot Type** (required): Wedding, Portrait, Event, etc.
- **Location** (optional): Where the shoot happened
- **Notes** (optional): Details about the shoot
- **Images Count** (optional): Number of photos taken

---

## 🐛 Troubleshooting

### Message not sending
- Check if you're logged in
- Check browser console for errors
- Ensure MongoDB is running
- Check /api/chat-requests endpoint returns data

### Preferences not showing
- Verify preferences document exists in MongoDB
- Check photographer_id matches
- Reload page after updating

### Admin not seeing messages
- Login as admin account
- Go to Chat Requests tab
- Refresh page
- Check MongoDB chat_requests collection

---

## 📚 File Locations

- **Backend Logic**: `app.py` (lines ~240-770)
- **Registration Form**: `templates/index.html` (lines ~75-130)
- **User Dashboard**: `templates/dashboard.html` (entire file)
- **Admin Dashboard**: `templates/admin_dashboard.html` (entire file)
- **Frontend Logic**: `static/script.js` (lines ~104-160, ~660-740)

---

## 🚀 Future Enhancements

- [ ] Email notifications for messages
- [ ] Real-time updates (WebSockets)
- [ ] Message attachments
- [ ] Shoot history charts/analytics
- [ ] AI recommendations based on history
- [ ] Message templates
- [ ] Bulk messaging
- [ ] Message search/archive

---

## 📞 Support

For issues or questions:
1. Check MongoDB connection
2. Review browser console for errors
3. Check server logs
4. Verify all files are saved correctly
5. Restart server

---

## 📸 NEW: Photo Analysis Storage Feature

### For Users: Analyze & Store Photos

1. **Analyze a Scene**
   - Dashboard → Click AI Scene Analyzer icon
   - Click "Start Camera" or "Upload Image"
   - Capture photo or select file
   - Click "Capture & Analyze"
   - See: "Photo successfully analyzed and saved to your profile!"

2. **View Your Analyzed Photos**
   - API: `GET /api/analyzed-photos`
   - Returns: List of all your analyzed photos

3. **Delete a Photo**
   - API: `DELETE /api/analyzed-photos/{photo_id}`
   - Removes from MongoDB and file system

### Photo Storage Details
- **File Location**: `static/uploads/`
- **Filename Format**: `analyzed_photo_{user_id}_{YYYYMMDD_HHMMSS}.jpg`
- **Database**: `analyzed_photos` collection
- **Profile**: Added to `photographers.analyzed_photos` array

### API Quick Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/analyze-scene` | Analyze & store photo |
| GET | `/api/analyzed-photos` | Get your photos |
| DELETE | `/api/analyzed-photos/{id}` | Delete a photo |

### Code Examples

**Store Photo**
```javascript
fetch('/api/analyze-scene', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ image: base64Image })
})
```

**Get Photos**
```javascript
fetch('/api/analyzed-photos')
  .then(r => r.json())
  .then(d => console.log(d.analyzed_photos))
```

**Delete Photo**
```javascript
fetch(`/api/analyzed-photos/${photoId}`, { method: 'DELETE' })
```

### MongoDB Collection: analyzed_photos
```javascript
{
  _id: ObjectId,
  photographer_id: ObjectId,
  image_path: "uploads/analyzed_photo_...",
  filename: "analyzed_photo_...",
  analyzed_at: ISODate,
  analysis_notes: "Scene analyzed..."
}
```

---

## ✅ Verification Commands

```bash
# Check collections exist
mongo
> use photomind
> db.photographer_preferences.count()
> db.shoot_history.count()
> db.chat_requests.count()

# Check data structure
> db.chat_requests.findOne()
> db.photographer_preferences.findOne()
```

---

**Created**: January 21, 2026
**Version**: 1.0
**Status**: Ready for Testing
