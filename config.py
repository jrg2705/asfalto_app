import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SECRET_KEY: obligatorio en producción. Nunca uses el fallback en un servidor real.
    _secret = os.getenv("SECRET_KEY")
    if not _secret:
        # Solo para desarrollo local. En Render/producción DEBE existir la variable.
        import warnings
        warnings.warn(
            "SECRET_KEY no está definida. Usando valor temporal inseguro. "
            "Configura SECRET_KEY en las variables de entorno de producción.",
            UserWarning
        )
        _secret = "dev-only-insecure-key-change-me"
    SECRET_KEY = _secret

    # Configuración de la base de datos
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
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

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
