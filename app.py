# This is the first commit to setup remote access
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from utils.gemini_integration import get_gemini_response
from utils.send_whatsapp import send_whatsapp_message
from utils.db import init_db

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__) 

# Environment Configuration
# Enable debug mode if DEBUG is set to True in the .env file (default: True)
app.config['DEBUG'] = os.getenv("DEBUG", "True") == "True"

# Database Initialization
# Use the DATABASE_URI environment variable, or default to a local SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI", "sqlite:///chatbot.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db, MenuItem = init_db(app)

# Optional: Create tables automatically on first request
@app.before_request
def create_tables():
    db.create_all()


# Menu Routes
@app.route('/menu', methods=['GET'])
def get_menu():
    """Get all menu items"""
    try:
        items = MenuItem.query.all()
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch menu items: {str(e)}'}), 500

@app.route('/menu', methods=['POST'])
def add_menu_item():
    """Add a new menu item"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'price', 'category']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        new_item = MenuItem(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            category=data['category'],
            available=data.get('available', True)
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify(new_item.to_dict()), 201
    except ValueError:
        return jsonify({'error': 'Invalid price format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to add menu item: {str(e)}'}), 500

@app.route('/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    """Update an existing menu item"""
    try:
        item = MenuItem.query.get_or_404(item_id)
        data = request.get_json()
        
        if 'name' in data:
            item.name = data['name']
        if 'description' in data:
            item.description = data['description']
        if 'price' in data:
            item.price = float(data['price'])
        if 'category' in data:
            item.category = data['category']
        if 'available' in data:
            item.available = data['available']
            
        db.session.commit()
        return jsonify(item.to_dict()), 200
    except ValueError:
        return jsonify({'error': 'Invalid price format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update menu item: {str(e)}'}), 500

@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    """Delete a menu item"""
    try:
        item = MenuItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Menu item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete menu item: {str(e)}'}), 500

# This is a special token that 
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification challenge from WhatsApp
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge
        else:
            return 'Verification token mismatch', 403

    elif request.method == 'POST':
        data = request.get_json()
        print("Received message:", data)

        # Extract the 'value' object from the payload
        try:
            changes = data["entry"][0]["changes"][0]["value"]
        except (KeyError, IndexError, TypeError):
            return jsonify(status="error", message="Invalid payload structure"), 400

        # Check if this is a user message or a status update
        if "messages" in changes:
            try:
                user_number = changes["messages"][0]["from"]
                message_text = changes["messages"][0]["text"]["body"]
            except (KeyError, IndexError, TypeError):
                return jsonify(status="error", message="Invalid message payload"), 400

            print("Received message_text:", message_text)
            gemini_reply = get_gemini_response(message_text)
            print("Gemini response:", gemini_reply)
            send_whatsapp_message(user_number, gemini_reply)
            return jsonify(status='success', reply=gemini_reply), 200

        elif "statuses" in changes:
            # This payload is a status update (e.g., sent, delivered, read)
            print("Received status update:", changes["statuses"])
            return jsonify(status='status_ack'), 200

        else:
            return jsonify(status="error", message="Unrecognized event"), 400

# Basic "Hello, World!" endpoint. This is the endpoint that connects with the browser. 
@app.route("/")
def hello():
    return "Goku vs Vegeta"

if __name__ == "__main__":
    app.run()
