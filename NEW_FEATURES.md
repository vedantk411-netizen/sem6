# New Features Documentation

## Overview
This document describes the new features added to the PhotoMind application:
1. **Photographer Preferences Storage** - Stores specialization, experience level, and equipment
2. **Shoot History Tracking** - Tracks all shoots by each photographer
3. **Chat Request System** - User messages that display on admin dashboard

---

## 1. Photographer Preferences Storage

### What It Does
When photographers register, they can now specify their:
- **Experience Level**: Beginner, Intermediate, or Expert
- **Specialization**: Photography types they specialize in (Wedding, Portrait, Event, Outdoor, Product)
- **Equipment**: Camera brands and tools they use (Canon, Nikon, Sony, GoPro, DJI Drones)

### MongoDB Collection
**Collection Name**: `photographer_preferences`

**Schema**:
```json
{
  "_id": ObjectId,
  "photographer_id": ObjectId,
  "specialization": ["Wedding", "Portrait"],
  "experience_level": "intermediate",
  "equipment": ["Canon", "Nikon"],
  "created_at": timestamp,
  "updated_at": timestamp
}
```

### API Endpoints

#### Get Preferences
```
GET /api/preferences
Authentication: Required (User login)
Response: 200 OK
{
  "_id": "...",
  "photographer_id": "...",
  "specialization": [...],
  "experience_level": "...",
  "equipment": [...]
}
```

#### Update Preferences
```
PUT /api/preferences
Authentication: Required (User login)
Request Body:
{
  "specialization": ["Wedding", "Portrait"],
  "experience_level": "intermediate",
  "equipment": ["Canon"]
}
Response: 200 OK
{ "message": "Preferences updated successfully" }
```

### Registration Form Updates
The registration form now includes:
- Dropdown for Experience Level
- Checkboxes for Specialization
- Checkboxes for Equipment

All fields are optional - photographers can update them later.

---

## 2. Shoot History Tracking

### What It Does
Photographers can log their shooting sessions with details like:
- Shoot type (Wedding, Portrait, etc.)
- Location
- Notes
- Number of images captured
- Date and time

### MongoDB Collection
**Collection Name**: `shoot_history`

**Schema**:
```json
{
  "_id": ObjectId,
  "photographer_id": ObjectId,
  "shoots": [
    {
      "shoot_type": "Wedding",
      "location": "Central Park",
      "notes": "Beautiful sunset photos",
      "images_count": 250,
      "date": timestamp
    }
  ],
  "total_shoots": 15,
  "created_at": timestamp
}
```

### API Endpoints

#### Get Shoot History
```
GET /api/shoot-history
Authentication: Required (User login)
Response: 200 OK
{
  "photographer_id": "...",
  "shoots": [
    {
      "shoot_type": "Wedding",
      "location": "Location",
      "notes": "Notes",
      "images_count": 250,
      "date": "2026-01-21T..."
    }
  ],
  "total_shoots": 1
}
```

#### Add Shoot to History
```
POST /api/shoot-history
Authentication: Required (User login)
Request Body:
{
  "shoot_type": "Wedding",
  "location": "Central Park",
  "notes": "Beautiful sunset session",
  "images_count": 250
}
Response: 201 Created
{ "message": "Shoot history added successfully" }
```

---

## 3. Chat Request System

### What It Does
Photographers can send messages/requests to the admin from the dashboard:
- Send a subject and message
- Messages appear on admin dashboard in real-time
- Admin can mark as read, respond, or delete
- Status tracking (new, read, responded, closed)

### MongoDB Collection
**Collection Name**: `chat_requests`

**Schema**:
```json
{
  "_id": ObjectId,
  "photographer_id": ObjectId,
  "photographer_name": "John Doe",
  "photographer_email": "john@example.com",
  "subject": "Need help with lighting",
  "message": "How do I setup studio lighting?",
  "status": "new",
  "created_at": timestamp,
  "response": "Use a 3-point lighting setup...",
  "responded_at": timestamp
}
```

### API Endpoints

#### Create Chat Request (User)
```
POST /api/chat-requests
Authentication: Required (User login)
Request Body:
{
  "subject": "Need help with lighting",
  "message": "How do I setup studio lighting?"
}
Response: 201 Created
{
  "message": "Chat request sent successfully",
  "request_id": "..."
}
```

#### Get Chat Requests (Admin)
```
GET /api/chat-requests
Authentication: Required (Admin login)
Query Parameters:
  - status: all | new | read | responded | closed (optional)
Response: 200 OK
[
  {
    "_id": "...",
    "photographer_id": "...",
    "photographer_name": "John Doe",
    "photographer_email": "john@example.com",
    "subject": "...",
    "message": "...",
    "status": "new",
    "created_at": "...",
    "response": null,
    "responded_at": null
  }
]
```

#### Update Chat Request (Admin)
```
PUT /api/chat-requests/{request_id}
Authentication: Required (Admin login)
Request Body:
{
  "status": "responded",
  "response": "This is the admin's response..."
}
Response: 200 OK
{ "message": "Chat request updated successfully" }
```

#### Delete Chat Request (Admin)
```
DELETE /api/chat-requests/{request_id}
Authentication: Required (Admin login)
Response: 200 OK
{ "message": "Chat request deleted successfully" }
```

---

## Admin Dashboard Updates

### Chat Requests Tab
A new tab has been added to the admin dashboard with:

1. **Message Display**
   - Shows photographer name and email
   - Displays subject and message
   - Shows creation timestamp
   - Color-coded status badge

2. **Status Filters**
   - All
   - New (unread)
   - Read
   - Responded

3. **Admin Actions**
   - Mark as Read
   - Respond with message
   - Delete message

4. **Response Management**
   - Admin can type responses
   - Response timestamp is recorded
   - Photographer email is shown for reference

---

## User Dashboard Updates

### Send Message Button
- New "Send Message" button in the navigation bar (orange color)
- Opens a modal form to compose messages
- Messages are sent to admin with subject and content

---

## Database Changes

### New Collections Created Automatically
When you start the application, these collections are created:
1. `photographer_preferences` - Stores photographer preferences
2. `shoot_history` - Tracks shooting sessions
3. `chat_requests` - Stores user messages to admin

### Updated Collections
- `photographers` - Now includes `created_at` and `updated_at` timestamps

---

## Usage Examples

### Example 1: Register with Preferences
```javascript
// User registers with preferences
fetch('/api/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Jane Photographer',
    email: 'jane@example.com',
    password: 'secure_password',
    specialization: ['Wedding', 'Portrait'],
    experience_level: 'intermediate',
    equipment: ['Canon', 'Sony']
  })
})
```

### Example 2: Log a Shoot
```javascript
// User logs a shoot session
fetch('/api/shoot-history', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    shoot_type: 'Wedding',
    location: 'Hyatt Grand Hotel',
    notes: 'Beautiful outdoor ceremony',
    images_count: 350
  })
})
```

### Example 3: Send Message to Admin
```javascript
// User sends message to admin
fetch('/api/chat-requests', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    subject: 'Question about portfolio upload',
    message: 'How do I upload images to my portfolio?'
  })
})
```

### Example 4: Admin Responds to Message
```javascript
// Admin responds to a message
fetch('/api/chat-requests/REQUEST_ID', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    status: 'responded',
    response: 'You can upload images from the Poses tab in admin dashboard.'
  })
})
```

---

## Frontend Features

### Registration Form
- Split into two sections: Basic Info and Photography Preferences
- Preferences section has checkboxes and dropdown
- All validation happens on submit

### Admin Dashboard
- New "Chat Requests" tab at the top
- Filter buttons for message status
- Each message shows full details
- Quick action buttons (Mark as Read, Respond, Delete)
- Response section displays admin replies

### User Dashboard
- Orange "Send Message" button in navbar
- Modal form for composing messages
- Subject and message fields
- Submit and cancel buttons

---

## Security Features

✅ All endpoints require authentication:
- User endpoints require `user_id` in session
- Admin endpoints require `admin_logged_in` in session

✅ Password hashing with bcrypt for registration

✅ Object ID validation for MongoDB operations

✅ CORS-ready JSON responses

---

## Testing the Features

### Test 1: User Registration with Preferences
1. Click "Create Account"
2. Fill in name, email, password
3. Select experience level
4. Check specialization boxes
5. Check equipment boxes
6. Click "Sign Up"
7. Check MongoDB: `db.photographer_preferences.findOne()`

### Test 2: Send Message to Admin
1. Login as photographer
2. Click "Send Message" button
3. Enter subject and message
4. Click "Send Message"
5. Login as admin
6. Go to "Chat Requests" tab
7. See the message with "New" badge

### Test 3: Admin Responds
1. Click "Respond" button on a message
2. Type response in prompt
3. Message status changes to "Responded"
4. Response is displayed under the message

---

## Future Enhancements

Possible improvements:
- Email notifications when messages are received/responded
- Real-time updates using WebSockets
- Message attachments/file uploads
- Bulk messaging to photographers
- Scheduled messages
- Message search/archive
- Preferences recommendations based on AI analysis
- Shoot history analytics/dashboard
- Portfolio recommendations based on shoot history
