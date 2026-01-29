# Photo Analysis API Documentation

## Overview
Complete API reference for the photo analysis and storage feature.

---

## Endpoints

### 1. POST `/api/analyze-scene`

**Description:** Analyze a scene by uploading a photo. Stores the photo in user's profile and MongoDB.

**Authentication:** Required (logged-in user)

**Request:**
```http
POST /api/analyze-scene HTTP/1.1
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBD..."
}
```

**Request Body:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | String | Yes | Base64-encoded image (with or without data URI prefix) |

**Response (Success):**
```json
{
  "suggestion": "Photo successfully analyzed and saved to your profile! Scene analysis complete.",
  "photo_id": "507f1f77bcf86cd799439011",
  "image_path": "uploads/analyzed_photo_507f1f77bcf86cd799439011_20260122_143022.jpg"
}
```

**Response (Errors):**

| Status | Error | Reason |
|--------|-------|--------|
| 401 | `{"error": "Unauthorized"}` | User not logged in |
| 400 | `{"error": "No image provided"}` | Missing image in request |
| 500 | `{"error": "Failed to analyze scene: ..."}` | Processing error (see message) |

**Example JavaScript:**
```javascript
async function analyzeScene(base64Image) {
  try {
    const response = await fetch('/api/analyze-scene', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: base64Image })
    });

    const data = await response.json();
    
    if (response.ok) {
      console.log('Photo saved!');
      console.log('Photo ID:', data.photo_id);
      console.log('Image Path:', data.image_path);
      console.log('Message:', data.suggestion);
    } else {
      console.error('Error:', data.error);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}
```

**Stored Data:**
- File System: `static/uploads/analyzed_photo_{user_id}_{timestamp}.jpg`
- Database: `analyzed_photos` collection
- User Profile: Reference added to `photographers` collection

---

### 2. GET `/api/analyzed-photos`

**Description:** Retrieve all analyzed photos for the logged-in user.

**Authentication:** Required (logged-in user)

**Request:**
```http
GET /api/analyzed-photos HTTP/1.1
```

**Query Parameters:** None

**Response (Success):**
```json
{
  "analyzed_photos": [
    {
      "id": "507f1f77bcf86cd799439011",
      "image_path": "uploads/analyzed_photo_507f1f77bcf86cd799439011_20260122_143022.jpg",
      "filename": "analyzed_photo_507f1f77bcf86cd799439011_20260122_143022.jpg",
      "analyzed_at": "2026-01-22T14:30:22.000000",
      "analysis_notes": "Scene analyzed for photography recommendations"
    },
    {
      "id": "507f1f77bcf86cd799439012",
      "image_path": "uploads/analyzed_photo_507f1f77bcf86cd799439011_20260122_143055.jpg",
      "filename": "analyzed_photo_507f1f77bcf86cd799439011_20260122_143055.jpg",
      "analyzed_at": "2026-01-22T14:30:55.000000",
      "analysis_notes": "Scene analyzed for photography recommendations"
    }
  ]
}
```

**Response (Empty):**
```json
{
  "analyzed_photos": []
}
```

**Response (Errors):**

| Status | Error | Reason |
|--------|-------|--------|
| 401 | `{"error": "Unauthorized"}` | User not logged in |
| 500 | `{"error": "Failed to fetch analyzed photos"}` | Database error |

**Example JavaScript:**
```javascript
async function getAnalyzedPhotos() {
  try {
    const response = await fetch('/api/analyzed-photos');
    const data = await response.json();
    
    if (response.ok) {
      console.log('Photos:', data.analyzed_photos);
      data.analyzed_photos.forEach(photo => {
        console.log(`${photo.filename} - ${photo.analyzed_at}`);
      });
    } else {
      console.error('Error:', data.error);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}
```

**Note:** Results are sorted by `analyzed_at` in descending order (most recent first).

---

### 3. DELETE `/api/analyzed-photos/<photo_id>`

**Description:** Delete an analyzed photo from user's profile and storage.

**Authentication:** Required (logged-in user)

**Request:**
```http
DELETE /api/analyzed-photos/507f1f77bcf86cd799439011 HTTP/1.1
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| photo_id | String | Yes | ObjectId of the photo to delete |

**Response (Success):**
```json
{
  "message": "Photo deleted successfully"
}
```

**Response (Errors):**

| Status | Error | Reason |
|--------|-------|--------|
| 401 | `{"error": "Unauthorized"}` | User not logged in |
| 404 | `{"error": "Photo not found"}` | Photo doesn't exist or not owned by user |
| 500 | `{"error": "Failed to delete photo"}` | Deletion error |

**Example JavaScript:**
```javascript
async function deletePhoto(photoId) {
  try {
    const response = await fetch(`/api/analyzed-photos/${photoId}`, {
      method: 'DELETE'
    });

    const data = await response.json();
    
    if (response.ok) {
      console.log('Photo deleted successfully');
      console.log(data.message);
    } else {
      console.error('Error:', data.error);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}
```

**Process:**
1. Verifies photo ownership (photographer_id check)
2. Deletes image file from `static/uploads/`
3. Removes record from `analyzed_photos` collection
4. Returns success message

---

## Data Models

### Analyzed Photo Object
```javascript
{
  "id": "string (ObjectId)",
  "image_path": "string (relative path)",
  "filename": "string",
  "analyzed_at": "string (ISO 8601 datetime)",
  "analysis_notes": "string"
}
```

### MongoDB Document Structure
```javascript
// In analyzed_photos collection:
{
  "_id": ObjectId,
  "photographer_id": ObjectId,
  "image_path": "uploads/analyzed_photo_...",
  "filename": "analyzed_photo_...",
  "analyzed_at": ISODate("2026-01-22T14:30:22.000Z"),
  "analysis_notes": "Scene analyzed for photography recommendations"
}

// In photographers collection (analyzed_photos array):
{
  "_id": ObjectId,
  "name": "John Doe",
  "email": "john@example.com",
  // ... other fields ...
  "analyzed_photos": [
    {
      "photo_id": ObjectId,
      "image_path": "uploads/analyzed_photo_...",
      "analyzed_at": ISODate("2026-01-22T14:30:22.000Z")
    }
  ]
}
```

---

## Authentication

All endpoints require the user to be logged in. The session is maintained via:
- Session cookie: `session` (Flask session management)
- Session data: `user_id` field must be present

**How to check authentication:**
```javascript
// Server-side (Python)
if 'user_id' not in session:
    return jsonify({'error': 'Unauthorized'}), 401
```

---

## File Storage

### Directory Structure
```
static/
└── uploads/
    ├── analyzed_photo_507f1f77bcf86cd799439011_20260122_143022.jpg
    ├── analyzed_photo_507f1f77bcf86cd799439011_20260122_143055.jpg
    └── analyzed_photo_507f1f77bcf86cd799439011_20260122_143100.jpg
```

### Filename Format
```
analyzed_photo_{user_id}_{timestamp}.jpg
```

**Example:**
```
analyzed_photo_507f1f77bcf86cd799439011_20260122_143022.jpg
                └─ user_id ─┘         └─── timestamp ──┘
```

**Timestamp Format:** `YYYYMMDD_HHMMSS`
- `20260122_143022` = January 22, 2026 at 14:30:22 (2:30 PM)

---

## Error Handling

### Common Errors

**401 Unauthorized**
```json
{"error": "Unauthorized"}
```
Solution: Log in first

**400 Bad Request**
```json
{"error": "No image provided"}
```
Solution: Ensure image parameter is included and valid

**404 Not Found**
```json
{"error": "Photo not found"}
```
Solution: Photo doesn't exist or belongs to another user

**500 Server Error**
```json
{"error": "Failed to analyze scene: [error details]"}
```
Solution: Check server logs, retry, or contact support

---

## Workflow Example

### Complete Flow: Capture → Store → Retrieve → Delete

```javascript
// Step 1: User captures photo from camera
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
context.drawImage(video, 0, 0, canvas.width, canvas.height);
const base64Image = canvas.toDataURL('image/jpeg');

// Step 2: Send to server for analysis and storage
const analyzeResponse = await fetch('/api/analyze-scene', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ image: base64Image })
});
const analyzeData = await analyzeResponse.json();
console.log('Photo stored with ID:', analyzeData.photo_id);

// Step 3: Later, retrieve all photos
const retrieveResponse = await fetch('/api/analyzed-photos');
const retrieveData = await retrieveResponse.json();
console.log('User has', retrieveData.analyzed_photos.length, 'analyzed photos');

// Step 4: Delete a specific photo
const deleteResponse = await fetch(`/api/analyzed-photos/${analyzeData.photo_id}`, {
  method: 'DELETE'
});
const deleteData = await deleteResponse.json();
console.log(deleteData.message); // "Photo deleted successfully"
```

---

## Rate Limiting
No rate limiting is currently implemented. Implement if needed for production.

---

## CORS
If accessing from different domains, ensure CORS is configured in Flask app.

---

## Troubleshooting

### Photo not saving
- Check if `static/uploads/` directory exists and is writable
- Verify user is logged in (check session)
- Check server logs for detailed error messages

### Photo not appearing in MongoDB
- Ensure MongoDB service is running
- Check MongoDB connection string
- Verify `analyzed_photos` collection exists

### Large file issues
- Base64 encoding can increase file size ~33%
- Consider implementing file size limits
- Monitor memory usage on server

### Timestamp issues
- Server timestamps use UTC
- Client receives ISO 8601 format
- Convert as needed in frontend

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-22 | Initial implementation |

---

## Support
For issues or questions:
1. Check server logs: `python app.py`
2. Verify MongoDB connection
3. Ensure all imports are installed (Pillow, Flask, pymongo)
4. Test endpoints individually using curl or Postman
