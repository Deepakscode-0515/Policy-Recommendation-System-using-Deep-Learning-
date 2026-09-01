import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret")
    # Use a MySQL 8 URL with PyMySQL driver. Prefer DATABASE_URL env var; default uses root:root on 127.0.0.1
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:root@127.0.0.1:3306/insurance_app"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    # Optional: tune Gemini model
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
