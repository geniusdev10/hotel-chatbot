import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Remove the Flask app initialization since it's in app.py
# Instead, create a function to initialize the database with an existing app
def init_db(app):
    db = SQLAlchemy(app)
    
    # Define a model for a menu item
    class MenuItem(db.Model):
        __tablename__ = 'menu_items'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.String(255))
        price = db.Column(db.Float, nullable=False)
        category = db.Column(db.String(50), nullable=False)
        available = db.Column(db.Boolean, default=True)
        is_veg = db.Column(db.Boolean, default=True)

        def to_dict(self):
            """Convert the MenuItem instance to a dictionary for JSON responses."""
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "price": self.price,
                "category": self.category,
                "available": self.available
            }
    
    return db, MenuItem

