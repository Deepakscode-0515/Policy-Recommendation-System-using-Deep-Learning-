import json
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Profile, Assessment
from utils import compute_raf, format_inr
from services.gemini_client import get_health_insights_and_policies

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

@app.template_filter("inr")
def inr_filter(val):
    return format_inr(val)

@app.template_filter("loadjson")
def loadjson_filter(val):
    try:
        return json.loads(val)
    except:
        return {}

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# @app.before_first_request
# def init_db():
#     db.create_all()

@app.route("/")
def index():
    if current_user.is_authenticated:
        # Recent assessments for dashboard
        recent = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).limit(5).all()
        return render_template("dashboard.html", recent=recent)
    return render_template("landing.html")

# Auth
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for("register"))
        user = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Registration successful. Please complete your profile.", "success")
        return redirect(url_for("edit_profile"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("index"))
        flash("Invalid credentials.", "error")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("index"))

# Profile
@app.route("/profile", methods=["GET"])
@login_required
def view_profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    return render_template("profile.html", profile=profile, mode="view")

@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if request.method == "POST":
        full_name = request.form.get("full_name") or ""
        age = int(request.form.get("age") or 0)
        gender = request.form.get("gender") or "other"
        health_issues = request.form.get("health_issues") or ""
        smoking = bool(request.form.get("smoking"))
        alcohol = bool(request.form.get("alcohol"))
        annual_income_inr = int(request.form.get("annual_income_inr") or 0)

        if not full_name or age <= 0 or annual_income_inr < 0:
            flash("Please provide valid name, age, and annual income (INR).", "error")
            return redirect(url_for("edit_profile"))

        if not profile:
            profile = Profile(
                user_id=current_user.id,
                full_name=full_name,
                age=age,
                gender=gender,
                health_issues=health_issues,
                smoking=smoking,
                alcohol=alcohol,
                annual_income_inr=annual_income_inr,
            )
            db.session.add(profile)
        else:
            profile.full_name = full_name
            profile.age = age
            profile.gender = gender
            profile.health_issues = health_issues
            profile.smoking = smoking
            profile.alcohol = alcohol
            profile.annual_income_inr = annual_income_inr
        db.session.commit()
        flash("Profile saved.", "success")
        return redirect(url_for("view_profile"))
    return render_template("profile.html", profile=profile, mode="edit")

# Assessments
@app.route("/assessments", methods=["GET"])
@login_required
def list_assessments():
    items = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).all()
    return render_template("assessments.html", items=items)

@app.route("/assessments/new", methods=["GET", "POST"])
@login_required
def new_assessment():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        flash("Please complete your profile before running an assessment.", "error")
        return redirect(url_for("edit_profile"))

    if request.method == "POST":
        # Snapshot profile dict
        p = {
            "full_name": profile.full_name,
            "age": profile.age,
            "gender": profile.gender,
            "health_issues": profile.health_issues,
            "smoking": profile.smoking,
            "alcohol": profile.alcohol,
            "annual_income_inr": profile.annual_income_inr,
        }
        raf_score = compute_raf(p)
        ai_json = get_health_insights_and_policies(p, raf_score)

        assessment = Assessment(
            user_id=current_user.id,
            raf_score=raf_score,
            input_snapshot_json=json.dumps(p, ensure_ascii=False),
            output_json=json.dumps(ai_json, ensure_ascii=False),
        )
        db.session.add(assessment)
        db.session.commit()
        flash("Assessment created.", "success")
        return redirect(url_for("list_assessments"))

    return render_template("assessment_new.html", profile=profile)

@app.route("/assessments/delete/<int:aid>", methods=["POST"])
@login_required
def delete_assessment(aid):
    item = Assessment.query.filter_by(id=aid, user_id=current_user.id).first()
    if not item:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Assessment deleted.", "success")
    return redirect(url_for("list_assessments"))

if __name__ == "__main__":
    app.run(debug=True)
