import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    # Configuración de la base de datos: usa la URL de Render si está disponible, si no, usa SQLite local.
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        # Añadir sslmode=require para conexiones a Render
        if "?sslmode" not in DATABASE_URL:
            DATABASE_URL += "?sslmode=require"
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///instance/site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = bool(int(os.getenv("MAIL_USE_TLS", 1)))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_TO = os.getenv("MAIL_TO")
