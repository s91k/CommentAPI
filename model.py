import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Comment(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), unique=False, nullable=False)
    DateTime = db.Column(db.DateTime, unique=False, nullable=False)
    Text = db.Column(db.String(200), unique=False, nullable=False)