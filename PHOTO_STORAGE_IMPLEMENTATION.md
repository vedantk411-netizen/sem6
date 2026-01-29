# Photo Analysis Storage Implementation

## Overview
When a user clicks to analyze a scene in the camera interface, the photo is now automatically stored in MongoDB and saved to the user's profile.

## Features Implemented

### 1. **New API Endpoint: `/api/analyze-scene` (POST)**
   - **Location:** `app.py` (lines 191-262)
   - **Functionality:**
     - Accepts base64-encoded image from the camera UI
     - Decodes and saves image to `static/uploads/` folder with timestamp
     - Stores photo metadata in MongoDB `analyzed_photos` collection
     - Adds photo reference to user's profile in `photographers` collection
   - **Returns:**
     - Success message
     - Photo ID from MongoDB
     - Image path for display

### 2. **New MongoDB Collection: `analyzed_photos`**
   - **Fields:**
     - `photographer_id` - References the photographer
     - `image_path` - Relative path to stored image
     - `filename` - Unique filename with timestamp
     - `analyzed_at` - Timestamp of analysis
     - `analysis_notes` - Notes about the analysis

### 3. **User Profile Enhancement**
   - Photographer documents now include an `analyzed_photos` array
   - Each entry contains:
     - `photo_id` - Reference to the analyzed_photos document
     - `image_path` - Path to the image
     - `analyzed_at` - When it was analyzed

### 4. **Retrieval Endpoints**

#### Get All Analyzed Photos
   - **Route:** `/api/analyzed-photos` (GET)
   - **Location:** `app.py` (lines 1034-1058)
   - **Authentication:** Required (user_id in session)
   - **Returns:** List of all analyzed photos for the current user

#### Delete Analyzed Photo
   - **Route:** `/api/analyzed-photos/<photo_id>` (DELETE)
   - **Location:** `app.py` (lines 1060-1095)
   - **Authentication:** Required
   - **Functionality:**
     - Verifies photo ownership
     - Deletes file from disk
     - Removes record from MongoDB
   - **Returns:** Success message or error

## Implementation Details

### File Storage
- Images are saved in `static/uploads/` directory
- Filename format: `analyzed_photo_{user_id}_{timestamp}.jpg`
- Example: `analyzed_photo_507f1f77bcf86cd799439011_20260122_143022.jpg`

### Database Storage
- Each analyzed photo creates two records:
  1. Document in `analyzed_photos` collection
  2. Entry in photographer's `analyzed_photos` array

### Data Flow
```
User captures photo in camera.html
     ↓
JavaScript sends base64 image to /api/analyze-scene
     ↓
Server decodes image and saves to disk
     ↓
Server stores metadata in MongoDB analyzed_photos collection
     ↓
Server adds reference to photographer's profile
     ↓
Response returns to client confirming storage
```

## Required Imports
The following imports were added to `app.py`:
```python
import base64      # For decoding base64 images
import io          # For BytesIO operations
from PIL import Image  # For image processing
```

## Usage Example

### Capturing and Storing a Photo
```javascript
// From camera.html
async function analyzeImage(base64Image) {
    const response = await fetch('/api/analyze-scene', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Image })
    });
    
    const data = await response.json();
    console.log('Photo saved:', data.image_path);
}
```

### Retrieving User's Analyzed Photos
```javascript
// Get all analyzed photos for current user
fetch('/api/analyzed-photos')
    .then(res => res.json())
    .then(data => {
        console.log('Analyzed photos:', data.analyzed_photos);
    });
```

### Deleting an Analyzed Photo
```javascript
// Delete a specific analyzed photo
fetch(`/api/analyzed-photos/${photo_id}`, {
    method: 'DELETE'
})
.then(res => res.json())
.then(data => console.log(data.message));
```

## Testing Checklist
- [ ] User logs in successfully
- [ ] Navigate to Camera UI
- [ ] Capture a photo or upload an image
- [ ] Click "Capture & Analyze" button
- [ ] Confirm "Photo successfully analyzed and saved to your profile!" message
- [ ] Check `static/uploads/` folder for saved image file
- [ ] Query MongoDB `analyzed_photos` collection to verify storage
- [ ] Call `/api/analyzed-photos` endpoint to retrieve photos
- [ ] Test deletion of analyzed photos

## Dependencies
Ensure the following Python packages are installed:
- `Flask` - Web framework
- `pymongo` - MongoDB driver
- `Pillow` - Image processing (required for PIL.Image)

Installation:
```bash
pip install Pillow
```

## Error Handling
- Returns 401 if user not logged in
- Returns 400 if no image provided
- Returns 500 with error message on processing failure
- Gracefully handles missing files on deletion

## Notes
- All photos are automatically tied to the logged-in user via `photographer_id`
- Photos include timestamps for chronological tracking
- Users cannot access or delete other users' photos (verified by photographer_id)
- Original image files are preserved on disk for potential future access
