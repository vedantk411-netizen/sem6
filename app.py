from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from pymongo import MongoClient, errors
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import bcrypt
import os
import random
import datetime
import base64
import io
from PIL import Image

app = Flask(__name__)
app.secret_key = 'dev_secret_key_fixed' # Fixed key to keep you logged in during server restarts

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to convert ObjectId to string for JSON serialization
def serialize_for_json(obj):
    """Recursively convert ObjectId to string in dictionaries and lists"""
    if isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

@app.route('/logout')
def logout():
    session.clear()  # Clears the user session
    return redirect(url_for('home'))  # Redirects to the homepage (ensure 'index' matches your view function name)

# Route for Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.clear()  # Clears the admin session
    return redirect(url_for('home'))  # Redirects to homepage


# MongoDB Connection
# Ensure your MongoDB service is running on the default port
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.server_info()  # will raise an exception if connection fails
    db = client['photomind']
    photographers_collection = db['photographers']
    admins_collection = db['admins']
    shoot_types_collection = db['shoot_types']
    poses_collection = db['poses']
    lighting_rules_collection = db['lighting_rules']
    ai_suggestions_collection = db['ai_suggestions']
    history_collection = db['user_history']
    chat_logs_collection = db['chat_logs']
    photographer_preferences_collection = db['photographer_preferences']
    shoot_history_collection = db['shoot_history']
    chat_requests_collection = db['chat_requests']
    analyzed_photos_collection = db['analyzed_photos']
    print("MongoDB connected successfully.")
except errors.ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    # Depending on your application's needs, you might want to exit or handle this differently.
    # For this example, we'll print the error and continue, though endpoints will fail.
    client = None
    photographers_collection = None
    admins_collection = None
    poses_collection = None
    lighting_rules_collection = None
    history_collection = None
    chat_logs_collection = None
    photographer_preferences_collection = None
    shoot_history_collection = None
    chat_requests_collection = None
    analyzed_photos_collection = None

# Global error handler to ensure JSON responses
@app.errorhandler(Exception)
def handle_error(error):
    """Catch all unhandled exceptions and return JSON"""
    print(f"[ERROR HANDLER] Caught exception: {error}")
    import traceback
    traceback.print_exc()
    return jsonify({'error': str(error), 'type': type(error).__name__}), 500

# Test endpoint to verify JSON is working
@app.route('/api/json-test', methods=['GET'])
def json_test():
    """Simple test to verify JSON responses work"""
    return jsonify({'status': 'ok', 'message': 'JSON responses working'}), 200

@app.route('/')
def home():
    is_logged_in = 'user_id' in session or 'admin_logged_in' in session
    shoot_types = list(shoot_types_collection.find()) if shoot_types_collection is not None else []
    shoot_types = serialize_for_json(shoot_types)
    return render_template('index.html', is_logged_in=is_logged_in, shoot_types=shoot_types)

@app.route('/dashboard.html')
def dashboard():
    # Ensure only logged-in users (photographers or admins) can access the dashboard
    if 'user_id' not in session and 'admin_logged_in' not in session:
        return redirect(url_for('home'))
    
    is_admin = 'admin_logged_in' in session
    shoot_types = list(shoot_types_collection.find()) if shoot_types_collection is not None else []
    shoot_types = serialize_for_json(shoot_types)
    return render_template('dashboard.html', is_admin=is_admin, shoot_types=shoot_types)

@app.route('/profile')
def profile():
    # Ensure only logged-in users can access their profile
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    return render_template('profile.html')

@app.route('/send-message')
def send_message():
    # Ensure only logged-in users can access message page
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    return render_template('send_message.html')

def get_shoot_data_internal(shoot_type, location_filter=None, lighting_filter=None):
    """Helper to fetch poses and rules for a specific shoot type."""
    poses = []
    rules = []
    
    if client is None:
        return poses, rules

    # Build query filters for the recommendation engine
    pose_query = {"category": "pose"}
    if location_filter:
        pose_query["location"] = location_filter
    if lighting_filter:
        pose_query["lighting"] = lighting_filter

    # 1. Check if a specific collection exists for this shoot type (New Architecture)
    if shoot_type in db.list_collection_names():
        specific_col = db[shoot_type]
        
        for p in specific_col.find(pose_query):
            p['_id'] = str(p['_id'])
            poses.append(p)
        for r in specific_col.find({"category": "rule"}):
            r['_id'] = str(r['_id'])
            rules.append(r)
    
    # 2. Fallback/Merge with global collections (Old Architecture)
    if poses_collection is not None:
        global_query = {'shoot_type': shoot_type}
        # Merge filters if your global collection supports them
        # global_query.update(pose_query) 
        
        for p in poses_collection.find(global_query):
            p['_id'] = str(p['_id'])
            poses.append(p)

    if lighting_rules_collection is not None:
        for r in lighting_rules_collection.find({'shoot_type': shoot_type}):
            r['_id'] = str(r['_id'])
            rules.append(r)
            
    return poses, rules

@app.route('/workspace.html')
def workspace():
    # Ensure only logged-in users (photographers or admins) can access the workspace
    if 'user_id' not in session and 'admin_logged_in' not in session:
        return redirect(url_for('home'))
    
    # Support for Jinja2: Fetch data if 'type' is in query params
    shoot_type = request.args.get('type')
    poses = []
    rules = []
    
    # Recommendation Engine: Analyze parameters
    # (In a real scenario, these could come from a form submission on the dashboard)
    location_param = request.args.get('location')
    lighting_param = request.args.get('lighting')

    if shoot_type:
        poses, rules = get_shoot_data_internal(shoot_type, location_param, lighting_param)
        poses = serialize_for_json(poses)
        rules = serialize_for_json(rules)
        
        # Log Session History for Personalization
        if 'user_id' in session and history_collection is not None:
            history_collection.insert_one({
                'user_id': session['user_id'],
                'action': 'view_workspace',
                'shoot_type': shoot_type,
                'params': {'location': location_param, 'lighting': lighting_param},
                'timestamp': datetime.datetime.now()
            })

    return render_template('workspace.html', shoot_type=shoot_type, poses=poses, rules=rules)

@app.route('/camera_ui')
def camera_ui():
    # Ensure only logged-in users (photographers or admins) can access the camera UI
    if 'user_id' not in session and 'admin_logged_in' not in session:
        return redirect(url_for('home'))
    
    return render_template('camera.html')

@app.route('/chatbot')
def chatbot_page():
    # Ensure only logged-in users (photographers or admins) can access the chatbot
    if 'user_id' not in session and 'admin_logged_in' not in session:
        return redirect(url_for('home'))
    return render_template('chatbot.html')

@app.route('/api/analyze-scene', methods=['POST'])
def analyze_scene():
    """Store analyzed scene photo in user profile and MongoDB"""
    try:
        # Check if user is logged in
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        base64_image = data.get('image')
        
        if not base64_image:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image and save to uploads folder
        import base64
        import io
        from PIL import Image
        
        # Remove the data:image/jpeg;base64, prefix if present
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
        
        # Decode image
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"analyzed_photo_{session['user_id']}_{timestamp}.jpg"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save image
        image.save(file_path)
        db_path = f"static/uploads/{filename}"
        
        # Store photo reference in MongoDB
        user_id = ObjectId(session['user_id'])
        photo_doc = {
            'photographer_id': user_id,
            'image_path': db_path,
            'filename': filename,
            'analyzed_at': datetime.datetime.now(),
            'analysis_notes': 'Scene analyzed for photography recommendations'
        }
        
        photo_id = None
        result = None
        
        # Insert into analyzed_photos collection
        if analyzed_photos_collection is not None:
            result = analyzed_photos_collection.insert_one(photo_doc)
            photo_id = str(result.inserted_id)
            print(f"Photo saved to MongoDB with ID: {photo_id}")
        
        # Add to user's profile
        if photographers_collection is not None and result is not None:
            try:
                # Initialize analyzed_photos array if it doesn't exist
                photographer_doc = photographers_collection.find_one({'_id': user_id})
                if photographer_doc and 'analyzed_photos' not in photographer_doc:
                    photographers_collection.update_one(
                        {'_id': user_id},
                        {'$set': {'analyzed_photos': []}}
                    )
                    print(f"Initialized analyzed_photos array for user {user_id}")
                
                # Add photo to analyzed_photos array
                photographers_collection.update_one(
                    {'_id': user_id},
                    {
                        '$push': {
                            'analyzed_photos': {
                                'photo_id': photo_id,
                                'image_path': db_path,
                                'analyzed_at': datetime.datetime.now()
                            }
                        }
                    }
                )
                print(f"Added photo to photographer profile: {photo_id}")
            except Exception as profile_error:
                print(f"Error updating photographer profile: {profile_error}")
        
        return jsonify({
            'suggestion': 'Photo successfully analyzed and saved to your profile! Scene analysis complete.',
            'photo_id': photo_id,
            'image_path': db_path
        }), 200
        
    except Exception as e:
        print(f"Error analyzing scene: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to analyze scene: {str(e)}'}), 500

@app.route('/api/workspace-data', methods=['GET'])
def get_workspace_data():
    # Ensure only logged-in users can access this data
    if 'user_id' not in session and 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    shoot_type = request.args.get('type')
    if not shoot_type:
        return jsonify({'error': 'Missing shoot type'}), 400
    
    location = request.args.get('location')
    lighting = request.args.get('lighting')
    
    poses, rules = get_shoot_data_internal(shoot_type, location, lighting)
    poses = serialize_for_json(poses)
    rules = serialize_for_json(rules)
    return jsonify({'poses': poses, 'rules': rules})

# --- Chatbot Module (Dynamic MongoDB + Keyword Matching) ---
@app.route('/api/chat', methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        shoot_type = data.get('shoot_type', None)  # Optional: filter by shoot type
        environment = data.get('environment', None)  # NEW: indoor or outdoor
        
        if not user_message:
            return jsonify({'response': "Please ask me something about photography."}), 400

        print(f"[CHAT] User: {user_message} | Shoot Type: {shoot_type} | Environment: {environment}")
        response = ""
        user_msg_lower = user_message.lower()
        
        # 1. Check if user is asking about a specific shoot type
        shoot_types_keywords = {
            'wedding': 'Wedding',
            'portrait': 'Portrait',
            'product': 'Product',
            'landscape': 'Landscape',
            'event': 'Event',
            'fashion': 'Fashion',
            'sports': 'Sports'
        }
        
        detected_shoot_type = None
        for keyword, st in shoot_types_keywords.items():
            if keyword in user_msg_lower:
                detected_shoot_type = st
                break
        
        # Use detected or provided shoot type
        active_shoot_type = detected_shoot_type or shoot_type
        
        # 2. Fetch relevant rules from MongoDB based on keywords, shoot type, AND environment
        try:
            if lighting_rules_collection is not None:
                query = {}
                
                # Build query based on keywords
                if 'lighting' in user_msg_lower or 'light' in user_msg_lower:
                    query['category'] = 'lighting'
                elif 'gear' in user_msg_lower or 'equipment' in user_msg_lower or 'lens' in user_msg_lower:
                    query['category'] = 'gear'
                elif 'composition' in user_msg_lower or 'compose' in user_msg_lower:
                    query['category'] = 'composition'
                elif 'focus' in user_msg_lower or 'sharp' in user_msg_lower or 'af' in user_msg_lower:
                    query['category'] = 'focus'
                elif 'settings' in user_msg_lower or 'iso' in user_msg_lower or 'aperture' in user_msg_lower or 'shutter' in user_msg_lower:
                    query['category'] = {'$in': ['gear', 'lighting']}  # Camera settings often in these categories
                
                # Filter by shoot type if detected or provided
                if active_shoot_type:
                    query['shoot_type'] = active_shoot_type
                
                # NEW: Filter by environment (indoor/outdoor) if provided
                if environment:
                    query['environment'] = environment
                    print(f"[CHAT] Filtering by environment: {environment}")
                
                # Fetch matching rules
                matching_rules = list(lighting_rules_collection.find(query).limit(3))
                
                if matching_rules:
                    # Combine multiple matching rules for comprehensive answer
                    response = " ".join([rule.get('rule', '') for rule in matching_rules])
                    
                    # Add settings if available
                    if matching_rules[0].get('camera_settings'):
                        settings = matching_rules[0]['camera_settings']
                        settings_text = ", ".join([f"{k}: {v}" for k, v in settings.items()])
                        response += f"\n\nRecommended Settings: {settings_text}"
                    
                    env_info = f" [{environment.upper()}]" if environment else ""
                    print(f"[CHAT] Found {len(matching_rules)} matching rule(s) from DB{env_info}")
                else:
                    # Fallback: return any rule for this shoot type & environment if no specific match
                    fallback_query = {}
                    if active_shoot_type:
                        fallback_query['shoot_type'] = active_shoot_type
                    if environment:
                        fallback_query['environment'] = environment
                    
                    any_rule = lighting_rules_collection.find_one(fallback_query)
                    if any_rule:
                        response = any_rule.get('rule', 'Ask me about photography!')
                    
        except Exception as e:
            print(f"[CHAT] DB error: {e}")
        
        # 3. Final fallback if no DB response
        if not response:
            if 'pose' in user_msg_lower or 'position' in user_msg_lower:
                response = "Posing Tip: Create angles with your body, use natural hand placement, and tilt your head slightly for flattering angles."
            elif 'outdoor' in user_msg_lower:
                response = "Outdoor Tip: Golden hour (sunrise/sunset) provides the most flattering light. Avoid harsh midday sun."
            elif 'indoor' in user_msg_lower:
                response = "Indoor Tip: Use window light or continuous lighting setups. High ISO (1600-3200) and fast lenses (f/2.0-f/2.8) help capture available light."
            elif 'color' in user_msg_lower or 'white balance' in user_msg_lower:
                response = "White Balance: Set WB correctly for your lighting. 5500K daylight, 3200K tungsten, or shoot in RAW for maximum flexibility."
            else:
                response = f"Ask me about lighting, poses, settings, composition, focus, gear, or any specific shoot type like wedding, portrait, product, landscape, event, fashion, or sports! 📸"
        
        # 4. Store chat in MongoDB for analytics
        try:
            if chat_logs_collection is not None:
                chat_logs_collection.insert_one({
                    'message': user_message,
                    'response': response,
                    'shoot_type': active_shoot_type,
                    'environment': environment,
                    'timestamp': datetime.datetime.now()
                })
                print(f"[CHAT] Logged to DB")
        except Exception as e:
            print(f"[CHAT] Log error: {e}")
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"[CHAT] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'response': "I'm having trouble. Please try again."}), 500

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' in session:
        return render_template('admin_dashboard.html')
    # If not logged in, redirect to home (where the login modal is)
    return redirect(url_for('home'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # Redirect to home as login is now unified in the main modal
    return redirect(url_for('home'))

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"Registering user: {data}") # Debug print
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'photographer')
        # Photographer preferences
        specialization = data.get('specialization', [])  # e.g., ['Wedding', 'Portrait', 'Event']
        experience_level = data.get('experience_level', 'beginner')  # beginner, intermediate, expert
        equipment = data.get('equipment', [])  # e.g., ['Canon', 'Nikon', 'Sony']

        if not name or not email or not password:
            return jsonify({'error': 'Missing fields'}), 400

        # Check if photographer already exists
        if photographers_collection.find_one({'email': email}):
            return jsonify({'error': 'Email already exists'}), 400

        # Hash the password securely
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create photographer document
        photographer = {
            'name': name,
            'email': email,
            'password': hashed_password, # Stored as binary hash
            'role': role,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }

        # Insert photographer
        result = photographers_collection.insert_one(photographer)
        photographer_id = result.inserted_id

        # Create and save preferences document
        if photographer_preferences_collection is not None:
            photographer_preferences_collection.insert_one({
                'photographer_id': photographer_id,
                'specialization': specialization,
                'experience_level': experience_level,
                'equipment': equipment,
                'created_at': datetime.datetime.now(),
                'updated_at': datetime.datetime.now()
            })
        
        # Initialize empty shoot history
        if shoot_history_collection is not None:
            shoot_history_collection.insert_one({
                'photographer_id': photographer_id,
                'shoots': [],
                'total_shoots': 0,
                'created_at': datetime.datetime.now()
            })

        return jsonify({'message': 'User registered successfully', 'user_id': str(photographer_id)}), 201
    except errors.PyMongoError as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database connection failed. Please ensure MongoDB is running.'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"Received login request: {data}")
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'photographer') # Check which role is attempting to login

        if not email or not password:
            return jsonify({'error': 'Missing credentials'}), 400

        user = None
        if role == 'admin':
            user = admins_collection.find_one({'email': email})
        else:
            user = photographers_collection.find_one({'email': email})
            
        print(f"User found in DB ({role}): {user}")

        # Verify password
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            print("Password check successful")
            
            # Set session based on role
            if role == 'admin':
                session['admin_logged_in'] = True
            else:
                session['user_id'] = str(user['_id'])

            return jsonify({
                'message': 'Login successful',
                'user': {
                    'name': user['name'],
                    'role': user.get('role', role)
                },
                'redirect': '/admin/dashboard' if role == 'admin' else '/dashboard.html'
            }), 200
        else:
            print("Password check failed")
            return jsonify({'error': 'Invalid credentials'}), 401
    except errors.PyMongoError as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database connection failed. Please ensure MongoDB is running.'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

# Admin - Shoot Types Management
@app.route('/api/shoot-types', methods=['GET'])
def get_shoot_types():
    if client is None or shoot_types_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
    
    shoot_types = []
    for shoot_type in shoot_types_collection.find():
        shoot_type['_id'] = str(shoot_type['_id'])
        shoot_types.append(shoot_type)
    return jsonify(shoot_types)

@app.route('/api/shoot-types', methods=['POST'])
def add_shoot_type():
    if client is None or shoot_types_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
        
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Missing name'}), 400
    
    icon = data.get('icon', 'fas fa-camera') # Default icon for new types
    description = data.get('description', 'Custom photography category')

    shoot_types_collection.insert_one({'name': name, 'icon': icon, 'description': description})
    return jsonify({'message': 'Shoot type added successfully'}), 201

@app.route('/api/shoot-types/<id>', methods=['PUT'])
def update_shoot_type(id):
    if client is None or shoot_types_collection is None:
        return jsonify({'error': 'Database not connected'}), 500

    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Missing name'}), 400

    result = shoot_types_collection.update_one({'_id': ObjectId(id)}, {'$set': {'name': name}})
    if result.matched_count == 0:
        return jsonify({'error': 'Shoot type not found'}), 404
    return jsonify({'message': 'Shoot type updated successfully'})

@app.route('/api/shoot-types/<id>', methods=['DELETE'])
def delete_shoot_type(id):
    if client is None or shoot_types_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
        
    result = shoot_types_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Shoot type not found'}), 404
    return jsonify({'message': 'Shoot type deleted successfully'})

# Admin - AI Suggestions Management
@app.route('/api/ai-suggestions', methods=['GET'])
def get_ai_suggestions():
    if client is None or ai_suggestions_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
    
    ai_suggestions = []
    for suggestion in ai_suggestions_collection.find():
        suggestion['_id'] = str(suggestion['_id'])
        ai_suggestions.append(suggestion)
    return jsonify(ai_suggestions)

@app.route('/api/ai-suggestions', methods=['POST'])
def add_ai_suggestion():
    if client is None or ai_suggestions_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
        
    data = request.get_json()
    suggestion_text = data.get('suggestion')
    if not suggestion_text:
        return jsonify({'error': 'Missing suggestion text'}), 400

    ai_suggestions_collection.insert_one({'suggestion': suggestion_text})
    return jsonify({'message': 'AI suggestion added successfully'}), 201

@app.route('/api/ai-suggestions/<id>', methods=['PUT'])
def update_ai_suggestion(id):
    if client is None or ai_suggestions_collection is None:
        return jsonify({'error': 'Database not connected'}), 500

    data = request.get_json()
    suggestion_text = data.get('suggestion')
    if not suggestion_text:
        return jsonify({'error': 'Missing suggestion text'}), 400

    result = ai_suggestions_collection.update_one({'_id': ObjectId(id)}, {'$set': {'suggestion': suggestion_text}})
    if result.matched_count == 0:
        return jsonify({'error': 'AI suggestion not found'}), 404
    return jsonify({'message': 'AI suggestion updated successfully'})

@app.route('/api/ai-suggestions/<id>', methods=['DELETE'])
def delete_ai_suggestion(id):
    if client is None or ai_suggestions_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
        
    result = ai_suggestions_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'AI suggestion not found'}), 404
    return jsonify({'message': 'AI suggestion deleted successfully'})

# Admin - Poses Management
@app.route('/api/poses', methods=['GET'])
def get_poses():
    if client is None or poses_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
    
    all_poses = []

    # 1. Fetch from Global Poses Collection (Old way)
    if poses_collection is not None:
        for pose in poses_collection.find():
            pose['_id'] = str(pose['_id'])
            all_poses.append(pose)

    # 2. Fetch from Specific Shoot Type Collections (New way)
    # This ensures images added to "Wedding", "Portrait", etc. appear in the portfolio
    if shoot_types_collection is not None:
        for t in shoot_types_collection.find():
            type_name = t.get('name')
            # Check if a collection exists for this shoot type
            # (We check both raw name and sanitized name to be safe)
            safe_name = "".join(x for x in type_name if x.isalnum() or x in " -_").strip()
            
            target_col_name = type_name if type_name in db.list_collection_names() else safe_name
            
            if target_col_name in db.list_collection_names():
                col = db[target_col_name]
                for p in col.find({"category": "pose"}):
                    p['_id'] = str(p['_id'])
                    # Inject shoot_type so the frontend knows where it belongs
                    if 'shoot_type' not in p:
                        p['shoot_type'] = type_name
                    all_poses.append(p)

    return jsonify(all_poses)

@app.route('/api/poses', methods=['POST'])
def upload_pose():
    if client is None or poses_collection is None:
        return jsonify({'error': 'Database not connected'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    shoot_type = request.form.get('shoot_type')
    name = request.form.get('name')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Store relative path for frontend access
        db_path = f"uploads/{filename}"
        
        poses_collection.insert_one({
            'name': name,
            'shoot_type': shoot_type,
            'image_path': db_path
        })
        return jsonify({'message': 'Pose uploaded successfully'}), 201

@app.route('/api/poses/<id>', methods=['DELETE'])
def delete_pose(id):
    if client is None:
        return jsonify({'error': 'Database not connected'}), 500
    
    try:
        pose_id = ObjectId(id)
    except:
        return jsonify({'error': 'Invalid ID format'}), 400

    # 1. Try deleting from Global Poses Collection
    if poses_collection is not None:
        if poses_collection.delete_one({'_id': pose_id}).deleted_count > 0:
            return jsonify({'message': 'Pose deleted successfully'})

    # 2. Try deleting from Specific Shoot Type Collections
    if shoot_types_collection is not None:
        for t in shoot_types_collection.find():
            type_name = t.get('name', '')
            if not type_name:
                continue

            # Check both raw name and sanitized name (to match how they are created)
            safe_name = "".join(x for x in type_name if x.isalnum() or x in " -_").strip()
            possible_names = {type_name, safe_name}
            
            for col_name in possible_names:
                if col_name and col_name in db.list_collection_names():
                    if db[col_name].delete_one({'_id': pose_id}).deleted_count > 0:
                        return jsonify({'message': 'Pose deleted successfully'})

    return jsonify({'error': 'Pose not found'}), 404

# Admin - Lighting Rules Management
@app.route('/api/lighting-rules', methods=['GET'])
def get_lighting_rules():
    if client is None or lighting_rules_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
    rules = []
    for rule in lighting_rules_collection.find():
        rule['_id'] = str(rule['_id'])
        rules.append(rule)
    return jsonify(rules)

@app.route('/api/lighting-rules', methods=['POST'])
def add_lighting_rule():
    if client is None or lighting_rules_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
    data = request.get_json()
    lighting_rules_collection.insert_one(data)
    return jsonify({'message': 'Lighting rule added successfully'}), 201

@app.route('/api/lighting-rules/<id>', methods=['DELETE'])
def delete_lighting_rule(id):
    if client is None or lighting_rules_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
    result = lighting_rules_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Rule not found'}), 404
    return jsonify({'message': 'Rule deleted successfully'})

# --- Chat Requests Management ---
@app.route('/api/chat-requests', methods=['POST'])
def create_chat_request():
    """User sends a chat request/message to admin"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        subject = data.get('subject', 'General Inquiry')
        message = data.get('message', '')
        
        if not message or len(message.strip()) == 0:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        if chat_requests_collection is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Get user info
        user = photographers_collection.find_one({'_id': ObjectId(session['user_id'])})
        
        chat_request_doc = {
            'photographer_id': ObjectId(session['user_id']),
            'photographer_name': user.get('name', 'Unknown') if user else 'Unknown',
            'photographer_email': user.get('email', 'unknown@email.com') if user else 'unknown@email.com',
            'subject': subject,
            'message': message,
            'status': 'new',  # new, read, responded, closed
            'created_at': datetime.datetime.now(),
            'response': None,
            'responded_at': None
        }
        
        result = chat_requests_collection.insert_one(chat_request_doc)
        
        return jsonify({
            'message': 'Chat request sent successfully',
            'request_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        print(f"Error creating chat request: {e}")
        return jsonify({'error': 'Failed to send message'}), 500

@app.route('/api/chat-requests', methods=['GET'])
def get_chat_requests():
    """Admin fetches all chat requests"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        if chat_requests_collection is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Get filter from query params (e.g., ?status=new)
        status_filter = request.args.get('status')
        query = {} if not status_filter else {'status': status_filter}
        
        requests = []
        for req in chat_requests_collection.find(query).sort('created_at', -1):
            req['_id'] = str(req['_id'])
            req['photographer_id'] = str(req['photographer_id'])
            req['created_at'] = req['created_at'].isoformat()
            if req['responded_at']:
                req['responded_at'] = req['responded_at'].isoformat()
            requests.append(req)
        
        return jsonify(requests), 200
    except Exception as e:
        print(f"Error fetching chat requests: {e}")
        return jsonify({'error': 'Failed to fetch requests'}), 500


@app.route('/api/my-chat-requests', methods=['GET'])
def get_my_chat_requests():
    """Return chat requests for the currently logged-in photographer"""
    print("[my-chat-requests] ENDPOINT CALLED")
    
    # Check session first
    if 'user_id' not in session:
        print("[my-chat-requests] No user_id in session, returning 401")
        return jsonify({'error': 'Unauthorized', 'chat_requests': []}), 401

    # Check if collection exists
    if chat_requests_collection is None:
        print("[my-chat-requests] chat_requests_collection is None!")
        return jsonify({'error': 'Database not connected', 'chat_requests': []}), 503

    user_id = session['user_id']
    print(f"[my-chat-requests] user_id from session: {user_id}")
    
    # Try to convert to ObjectId, but have fallback
    try:
        user_oid = ObjectId(user_id)
        print(f"[my-chat-requests] Successfully converted to ObjectId: {user_oid}")
    except Exception as oid_err:
        print(f"[my-chat-requests] Could not convert to ObjectId: {oid_err}, using string ID")
        user_oid = user_id
    
    # Query the database
    try:
        print(f"[my-chat-requests] Querying with photographer_id: {user_oid}")
        requests = []
        cursor = chat_requests_collection.find({'photographer_id': user_oid}).sort('created_at', -1)
        
        for req in cursor:
            req['_id'] = str(req['_id'])
            req['photographer_id'] = str(req['photographer_id'])
            req['created_at'] = req['created_at'].isoformat() if req.get('created_at') else ''
            if req.get('responded_at'):
                req['responded_at'] = req['responded_at'].isoformat()
            requests.append(req)
        
        print(f"[my-chat-requests] Found {len(requests)} requests, returning 200")
        response = jsonify({'chat_requests': requests})
        response.headers['Content-Type'] = 'application/json'
        return response, 200
        
    except Exception as query_err:
        print(f"[my-chat-requests] Query failed: {query_err}")
        import traceback
        traceback.print_exc()
        error_response = jsonify({'error': str(query_err), 'chat_requests': []})
        error_response.headers['Content-Type'] = 'application/json'
        return error_response, 500

@app.route('/api/chat-requests/<request_id>', methods=['PUT'])
def update_chat_request(request_id):
    """Admin updates chat request status and response"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        status = data.get('status')  # new, read, responded, closed
        response = data.get('response')
        
        if chat_requests_collection is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        update_data = {'status': status} if status else {}
        if response:
            update_data['response'] = response
            update_data['responded_at'] = datetime.datetime.now()
        
        result = chat_requests_collection.update_one(
            {'_id': ObjectId(request_id)},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Request not found'}), 404
        
        return jsonify({'message': 'Chat request updated successfully'}), 200
    except Exception as e:
        print(f"Error updating chat request: {e}")
        return jsonify({'error': 'Failed to update request'}), 500

@app.route('/api/chat-requests/<request_id>', methods=['DELETE'])
def delete_chat_request(request_id):
    """Admin deletes a chat request"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        if chat_requests_collection is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        result = chat_requests_collection.delete_one({'_id': ObjectId(request_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Request not found'}), 404
        
        return jsonify({'message': 'Chat request deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting chat request: {e}")
        return jsonify({'error': 'Failed to delete request'}), 500

# --- Photographer Preferences Management ---
@app.route('/api/preferences', methods=['GET'])
def get_preferences():
    """Get photographer's preferences"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        if photographer_preferences_collection is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        prefs = photographer_preferences_collection.find_one({
            'photographer_id': ObjectId(session['user_id'])
        })
        
        if not prefs:
            return jsonify({'error': 'Preferences not found'}), 404
        
        prefs['_id'] = str(prefs['_id'])
        prefs['photographer_id'] = str(prefs['photographer_id'])
        prefs['created_at'] = prefs['created_at'].isoformat()
        prefs['updated_at'] = prefs['updated_at'].isoformat()
        
        return jsonify(prefs), 200
    except Exception as e:
        print(f"Error fetching preferences: {e}")
        return jsonify({'error': 'Failed to fetch preferences'}), 500

@app.route('/api/preferences', methods=['PUT'])
def update_preferences():
    """Update photographer's preferences"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        if photographer_preferences_collection is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        update_data = {
            'specialization': data.get('specialization', []),
            'experience_level': data.get('experience_level', 'beginner'),
            'equipment': data.get('equipment', []),
            'updated_at': datetime.datetime.now()
        }
        
        result = photographer_preferences_collection.update_one(
            {'photographer_id': ObjectId(session['user_id'])},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Preferences not found'}), 404
        
        return jsonify({'message': 'Preferences updated successfully'}), 200
    except Exception as e:
        print(f"Error updating preferences: {e}")
        return jsonify({'error': 'Failed to update preferences'}), 500

# --- Shoot History Management ---
@app.route('/api/shoot-history', methods=['GET'])
def get_shoot_history():
    """Get photographer's shoot history"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        if shoot_history_collection is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        history = shoot_history_collection.find_one({
            'photographer_id': ObjectId(session['user_id'])
        })
        
        if not history:
            return jsonify({'shoots': [], 'total_shoots': 0}), 200
        
        history['_id'] = str(history['_id'])
        history['photographer_id'] = str(history['photographer_id'])
        history['created_at'] = history['created_at'].isoformat()
        
        return jsonify(history), 200
    except Exception as e:
        print(f"Error fetching shoot history: {e}")
        return jsonify({'error': 'Failed to fetch history'}), 500

@app.route('/api/shoot-history', methods=['POST'])
def add_shoot_history():
    """Add a shoot session to history"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        shoot_type = data.get('shoot_type')
        location = data.get('location', 'Unknown')
        notes = data.get('notes', '')
        images_count = data.get('images_count', 0)
        
        if not shoot_type:
            return jsonify({'error': 'shoot_type is required'}), 400
        
        if shoot_history_collection is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        shoot_entry = {
            'shoot_type': shoot_type,
            'location': location,
            'notes': notes,
            'images_count': images_count,
            'date': datetime.datetime.now()
        }
        
        result = shoot_history_collection.update_one(
            {'photographer_id': ObjectId(session['user_id'])},
            {
                '$push': {'shoots': shoot_entry},
                '$inc': {'total_shoots': 1}
            }
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Shoot history not found'}), 404
        
        return jsonify({'message': 'Shoot history added successfully'}), 201
    except Exception as e:
        print(f"Error adding shoot history: {e}")
        return jsonify({'error': 'Failed to add shoot history'}), 500

# --- User Profile ---
@app.route('/api/profile', methods=['GET'])
def get_user_profile():
    """Get complete user profile with preferences and history"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user_id = ObjectId(session['user_id'])
        
        # Get photographer info
        photographer = photographers_collection.find_one({'_id': user_id})
        if not photographer:
            return jsonify({'error': 'Photographer not found'}), 404
        
        # Get preferences
        preferences = None
        if photographer_preferences_collection is not None:
            preferences = photographer_preferences_collection.find_one({'photographer_id': user_id})
        
        # Get shoot history
        history = None
        if shoot_history_collection is not None:
            history = shoot_history_collection.find_one({'photographer_id': user_id})
        
        # Build profile response
        profile = {
            'id': str(photographer['_id']),
            'name': photographer.get('name', 'N/A'),
            'email': photographer.get('email', 'N/A'),
            'role': photographer.get('role', 'photographer'),
            'created_at': photographer.get('created_at', '').isoformat() if photographer.get('created_at') else '',
            'preferences': None,
            'shoot_history': None,
            'analyzed_photos': []
        }
        
        # Add preferences if exists
        if preferences is not None:
            profile['preferences'] = {
                'specialization': preferences.get('specialization', []),
                'experience_level': preferences.get('experience_level', 'beginner'),
                'equipment': preferences.get('equipment', []),
                'updated_at': preferences.get('updated_at', '').isoformat() if preferences.get('updated_at') else ''
            }
        
        # Add shoot history if exists
        if history is not None:
            shoots = []
            for shoot in history.get('shoots', []):
                shoots.append({
                    'shoot_type': shoot.get('shoot_type', ''),
                    'location': shoot.get('location', ''),
                    'notes': shoot.get('notes', ''),
                    'images_count': shoot.get('images_count', 0),
                    'date': shoot.get('date', '').isoformat() if shoot.get('date') else ''
                })
            
            profile['shoot_history'] = {
                'shoots': shoots,
                'total_shoots': history.get('total_shoots', 0)
            }
        
        # Add analyzed photos if collection exists
        if analyzed_photos_collection is not None:
            analyzed_photos = []
            for photo in analyzed_photos_collection.find({'photographer_id': user_id}).sort('analyzed_at', -1):
                analyzed_photos.append({
                    'id': str(photo['_id']),
                    'image_path': photo.get('image_path', ''),
                    'filename': photo.get('filename', ''),
                    'analyzed_at': photo.get('analyzed_at', '').isoformat() if photo.get('analyzed_at') else ''
                })
            profile['analyzed_photos'] = analyzed_photos
        
        return jsonify(profile), 200
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return jsonify({'error': 'Failed to fetch profile'}), 500


@app.route('/api/profile/avatar', methods=['POST'])
def upload_avatar():
    """Upload a profile avatar for the logged-in user."""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    if client is None or photographers_collection is None:
        return jsonify({'error': 'Database not connected'}), 500

    if 'avatar' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        print(f"[upload_avatar] called. session_user={session.get('user_id')}")
        print(f"[upload_avatar] request.files keys: {list(request.files.keys())}")

        filename = secure_filename(f"{session['user_id']}_{int(datetime.datetime.now().timestamp())}_{file.filename}")
        save_dir = app.config.get('UPLOAD_FOLDER', 'static/uploads')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        try:
            file.save(save_path)
        except Exception as save_err:
            print(f"[upload_avatar] Error saving file to disk: {save_err}")
            return jsonify({'error': f'Failed to save file: {str(save_err)}'}), 500

        # Validate and normalize image using Pillow (convert to JPEG, resize if large)
        try:
            with Image.open(save_path) as img:
                img = img.convert('RGB')
                max_dim = 800
                if max(img.size) > max_dim:
                    img.thumbnail((max_dim, max_dim))
                img.save(save_path, format='JPEG', quality=85)
        except Exception as pil_err:
            print(f"[upload_avatar] Pillow error processing image: {pil_err}")
            return jsonify({'error': f'Invalid image file: {str(pil_err)}'}), 400

        # return path that the frontend can load directly
        db_path = f"static/uploads/{filename}"

        # update photographer record with image path
        try:
            # Prefer ObjectId but allow fallback to raw string _id if necessary
            try:
                phot_oid = ObjectId(session['user_id'])
                photographers_collection.update_one(
                    {'_id': phot_oid},
                    {'$set': {'image_path': db_path, 'updated_at': datetime.datetime.now()}}
                )
            except Exception as oid_err:
                print(f"[upload_avatar] ObjectId conversion failed: {oid_err}. Falling back to string id.")
                photographers_collection.update_one(
                    {'_id': session['user_id']},
                    {'$set': {'image_path': db_path, 'updated_at': datetime.datetime.now()}},
                    upsert=False
                )
        except Exception as db_err:
            print(f"[upload_avatar] DB update error: {db_err}")
            return jsonify({'error': f'Failed to update profile: {str(db_err)}'}), 500

        print(f"[upload_avatar] Saved avatar: {db_path}")
        return jsonify({'image_path': db_path}), 200
    except Exception as e:
        print(f"Error in upload_avatar: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to upload avatar: {str(e)}'}), 500


# --- Dev / Debug Endpoints (temporary) ---
@app.route('/dev/upload-avatar-test', methods=['POST'])
def dev_upload_avatar_test():
    """Dev endpoint: accept a file upload without auth and return saved path and image info."""
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file uploaded (dev)'}), 400

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'error': 'No file selected (dev)'}), 400

    try:
        filename = secure_filename(f"dev_{int(datetime.datetime.now().timestamp())}_{file.filename}")
        save_dir = app.config.get('UPLOAD_FOLDER', 'static/uploads')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        file.save(save_path)

        # Validate image
        try:
            with Image.open(save_path) as img:
                info = {'format': img.format, 'size': img.size, 'mode': img.mode}
        except Exception as img_err:
            return jsonify({'error': f'Invalid image file: {str(img_err)}'}), 400

        db_path = f"static/uploads/{filename}"
        return jsonify({'saved': db_path, 'info': info}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Dev upload failed: {str(e)}'}), 500


@app.route('/api/session-info', methods=['GET'])
def session_info():
    """Return current Flask session keys (for debugging only)."""
    try:
        return jsonify({'session': dict(session)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test-chat-requests', methods=['GET'])
def test_chat_requests():
    """Test endpoint to verify chat requests work (returns mock data)."""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'No user_id in session', 'user_id': None}), 401
        
        user_id = session['user_id']
        if chat_requests_collection is None:
            return jsonify({'error': 'chat_requests_collection is None'}), 500
        
        # Try to query
        try:
            user_oid = ObjectId(user_id)
        except:
            user_oid = user_id
        
        count = chat_requests_collection.count_documents({'photographer_id': user_oid})
        
        return jsonify({
            'test': 'success',
            'user_id': str(user_id),
            'collection_count': count,
            'db_connected': client is not None
        }), 200
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

# --- Analyzed Photos Management ---
@app.route('/api/analyzed-photos', methods=['GET'])
def get_analyzed_photos():
    """Get all analyzed photos for current user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        if analyzed_photos_collection is None:
            return jsonify({'analyzed_photos': []}), 200
        
        user_id = ObjectId(session['user_id'])
        photos = []
        
        for photo in analyzed_photos_collection.find({'photographer_id': user_id}).sort('analyzed_at', -1):
            photos.append({
                'id': str(photo['_id']),
                'image_path': photo.get('image_path'),
                'filename': photo.get('filename'),
                'analyzed_at': photo.get('analyzed_at', '').isoformat() if photo.get('analyzed_at') else '',
                'analysis_notes': photo.get('analysis_notes', '')
            })
        
        return jsonify({'analyzed_photos': photos}), 200
    except Exception as e:
        print(f"Error fetching analyzed photos: {e}")
        return jsonify({'error': 'Failed to fetch analyzed photos'}), 500

@app.route('/api/analyzed-photos/<photo_id>', methods=['DELETE'])
def delete_analyzed_photo(photo_id):
    """Delete an analyzed photo"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        if analyzed_photos_collection is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        user_id = ObjectId(session['user_id'])
        photo_obj_id = ObjectId(photo_id)
        
        # Verify ownership
        photo = analyzed_photos_collection.find_one({
            '_id': photo_obj_id,
            'photographer_id': user_id
        })
        
        if not photo:
            return jsonify({'error': 'Photo not found'}), 404
        
        # Delete file from disk
        file_path = photo.get('image_path')
        if file_path:
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], file_path.replace('uploads/', ''))
            try:
                if os.path.exists(full_path):
                    os.remove(full_path)
            except Exception as e:
                print(f"Warning: Could not delete file {full_path}: {e}")
        
        # Delete from MongoDB
        analyzed_photos_collection.delete_one({'_id': photo_obj_id})
        
        return jsonify({'message': 'Photo deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting analyzed photo: {e}")
        return jsonify({'error': 'Failed to delete photo'}), 500

# Admin - User Management
@app.route('/api/users', methods=['GET'])
def get_users():
    if client is None or photographers_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
    
    users = []
    for user in photographers_collection.find():
        user['_id'] = str(user['_id'])
        user.pop('password', None)  # Do not return password hash
        users.append(user)
    return jsonify(users)

@app.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
    if client is None or photographers_collection is None:
        return jsonify({'error': 'Database not connected'}), 500

    data = request.get_json()
    # Exclude password from being updated this way for security reasons
    update_data = {k: v for k, v in data.items() if k != 'password'}

    result = photographers_collection.update_one({'_id': ObjectId(id)}, {'$set': update_data})
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    if client is None or photographers_collection is None:
        return jsonify({'error': 'Database not connected'}), 500
        
    result = photographers_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted successfully'})

# Admin - Analytics
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    if client is None or photographers_collection is None or shoot_types_collection is None:
        return jsonify({'error': 'Database not connected'}), 500

    num_users = photographers_collection.count_documents({})
    num_shoot_types = shoot_types_collection.count_documents({})
    num_poses = poses_collection.count_documents({}) if poses_collection is not None else 0
    num_lighting_rules = lighting_rules_collection.count_documents({}) if lighting_rules_collection is not None else 0

    return jsonify({
        'num_users': num_users,
        'num_shoot_types': num_shoot_types,
        'num_poses': num_poses,
        'num_lighting_rules': num_lighting_rules
    })

def initialize_db():
    if client is None or admins_collection is None:
        return
        
    try:
        email = 'admin@photomind.com'
        password = 'password'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Upsert: Update if exists, Insert if not. This ensures password is always 'password' on restart.
        admins_collection.update_one(
            {'email': email},
            {'$set': {'name': 'Admin', 'password': hashed_password, 'role': 'admin'}},
            upsert=True
        )
        print(f"Admin user '{email}' ensured with password '{password}'.")
            
    except Exception as e:
        print(f"Error creating admin user: {e}")

    # Seed Default Shoot Types if collection is empty
    if shoot_types_collection is not None and shoot_types_collection.count_documents({}) == 0:
        defaults = [
            {"name": "Wedding", "icon": "fas fa-rings", "description": "Romantic lighting & candid moments"},
            {"name": "Portrait", "icon": "fas fa-user", "description": "Focus on facial features & depth"},
            {"name": "Outdoor", "icon": "fas fa-tree", "description": "Natural light & landscapes"},
            {"name": "Event", "icon": "fas fa-glass-cheers", "description": "Low light & dynamic action"},
            {"name": "Product", "icon": "fas fa-box-open", "description": "Studio lighting & details"},
            {"name": "Night", "icon": "fas fa-moon", "description": "Long exposure & ISO settings"},
            {"name": "Fashion", "icon": "fas fa-tshirt", "description": "Trendy styles & poses"}
        ]
        try:
            shoot_types_collection.insert_many(defaults)
            print("Seeded default shoot types.")
        except Exception as e:
            print(f"Error seeding shoot types: {e}")

if __name__ == '__main__':
    initialize_db()
    print("Starting Flask Server on port 5000...")
    app.run(debug=True, port=5000, use_reloader=False)
