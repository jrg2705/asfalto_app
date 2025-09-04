from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, logout_user
from config import Config
from models import db, SiteSetting, Service, Project, SuccessStory, ContactMessage, PopupMessage, User
from forms import ContactForm, FooterContactForm, LoginForm
from flask.cli import with_appcontext
import click
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}

@app.context_processor
def inject_footer_form():
    form = FooterContactForm()
    return {'footer_form': form}
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Para inicializar base desde CLI
@app.cli.command("create-db")
@with_appcontext
def create_db():
    db.create_all()
    click.echo("Base de datos creada.")

@app.cli.command("create-admin")
@with_appcontext
def create_admin():
    """Creates a new admin user."""
    username = click.prompt("Enter admin username")
    password = click.prompt("Enter admin password", hide_input=True, confirmation_prompt=True)
    
    user = User.query.filter_by(username=username).first()
    if user:
        click.echo(f"User '{{username}}' already exists.")
        return

    new_admin = User(username=username)
    new_admin.set_password(password)
    db.session.add(new_admin)
    db.session.commit()
    click.echo(f"Admin user '{{username}}' created successfully.")

@app.cli.command("seed-admin")
@with_appcontext
def seed_admin():
    """Creates a default admin user if none exists. USE ONLY FOR INITIAL DEPLOYMENT!"""
    from models import User, db # Import here to avoid circular dependency issues
    default_username = "admin"
    default_password = "adminpassword" # !!! CHANGE THIS IMMEDIATELY AFTER LOGIN !!!

    user = User.query.filter_by(username=default_username).first()
    if user:
        click.echo(f"Default admin user '{default_username}' already exists. Skipping seeding.")
        return

    new_admin = User(username=default_username)
    new_admin.set_password(default_password)
    db.session.add(new_admin)
    db.session.commit()
    click.echo(f"Default admin user '{default_username}' created successfully.")
    click.echo("!!! IMPORTANT: Log in immediately and change the password for 'admin' !!!")

# Clases de Vistas Seguras para Admin
class SecuredModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

# Panel Admin
admin = Admin(app, name="Panel Admin", template_mode="bootstrap4", index_view=MyAdminIndexView())

# Custom User ModelView
from wtforms import PasswordField
from wtforms.validators import DataRequired

class UserAdminView(SecuredModelView):
    column_list = ('username',) # Only show username in list view
    form_columns = ('username', 'password') # Show username and a new 'password' field in form

    form_extra_fields = {
        'password': PasswordField('Password', validators=[DataRequired()])
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data: # Only hash if password field is provided
            model.set_password(form.password.data)
        elif is_created:
            raise ValueError("Password is required for new users.")

        return super(UserAdminView, self).on_model_change(form, model, is_created)

admin.add_view(UserAdminView(User, db.session))

admin.add_view(SecuredModelView(SiteSetting, db.session))
admin.add_view(SecuredModelView(Service, db.session))
admin.add_view(SecuredModelView(Project, db.session))
admin.add_view(SecuredModelView(SuccessStory, db.session))
admin.add_view(SecuredModelView(ContactMessage, db.session))
admin.add_view(SecuredModelView(PopupMessage, db.session))

# --- Rutas de Autenticación ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Rutas públicas
@app.route("/")
def index():
    settings = SiteSetting.query.first()
    services = Service.query.all()
    projects = Project.query.all()
    success_stories = SuccessStory.query.all()
    popup = PopupMessage.query.filter_by(is_active=True).first()
    return render_template("index.html", settings=settings, services=services,
                           projects=projects, stories=success_stories, popup=popup)

@app.route("/services")
def services():
    services = Service.query.all()
    return render_template("services.html", services=services)

@app.route("/projects")
def projects():
    projects = Project.query.all()
    return render_template("projects.html", projects=projects)

@app.route("/project/<int:id>")
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template("project_detail.html", project=project)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact_msg = ContactMessage(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            company=form.company.data,
            inquiry_type=form.inquiry_type.data,
            message=form.message.data
        )
        db.session.add(contact_msg)
        db.session.commit()
        flash("Mensaje enviado correctamente. Gracias por contactarnos.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)


@app.route("/footer-contact", methods=["POST"])
def footer_contact():
    form = FooterContactForm()
    redirect_url = (request.referrer or url_for('index')).split('#')[0] + '#site-footer'

    if form.validate_on_submit():
        contact_msg = ContactMessage(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            city=form.city.data,
            province=form.province.data,
            message=form.comment.data
        )
        db.session.add(contact_msg)
        db.session.commit()
        flash("Gracias por contactarnos, te responderemos a la brevedad.", "success")
    else:
        flash("Hubo un error en tu formulario. Por favor, revisa los campos.", "danger")
    
    return redirect(redirect_url)


if __name__ == "__main__":
    app.run(debug=True)