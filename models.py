from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship("Profile", backref="user", uselist=False, cascade="all, delete-orphan")
    assessments = db.relationship("Assessment", backref="user", lazy=True, cascade="all, delete-orphan")

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    full_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)  # "male","female","other"
    health_issues = db.Column(db.Text, nullable=True)  # comma-separated or text
    smoking = db.Column(db.Boolean, default=False)
    alcohol = db.Column(db.Boolean, default=False)
    annual_income_inr = db.Column(db.Integer, nullable=False)  # INR as integer rupees

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Assessment(db.Model):
    __tablename__ = "assessments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    raf_score = db.Column(db.Float, nullable=False)
    input_snapshot_json = db.Column(db.Text, nullable=False)    # JSON string of input profile at the moment
    output_json = db.Column(db.Text, nullable=False)            # JSON string of AI response/recommendations
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
