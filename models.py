from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class SiteSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default="Mi Marca")
    logo_url = db.Column(db.String(255))
    primary_color = db.Column(db.String(20), default="#E2601B")

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    icon_url = db.Column(db.String(255))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

class SuccessStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    customer_or_category = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    inquiry_type = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    province = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text)

class PopupMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default="Mensaje Antes de Seguir")
    content = db.Column(db.Text, default="Este es un mensaje de bienvenida. Puedes editarlo desde el panel de administración.")
    button_text = db.Column(db.String(50), default="Entendido")
    is_active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<PopupMessage {self.title}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False, default='editor')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'