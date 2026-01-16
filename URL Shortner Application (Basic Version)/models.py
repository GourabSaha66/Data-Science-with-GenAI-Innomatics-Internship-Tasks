from flask_sqlalchemy import SQLAlchemy
import string
import random

db = SQLAlchemy()

class URLModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, original_url):
        self.original_url = original_url
        self.short_code = self.generate_short_code()

    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=6))