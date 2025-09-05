from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import LoginManager, current_user, login_user, logout_user
from config import Config
from models import db, SiteSetting, Service, Project, SuccessStory, ContactMessage, PopupMessage, User
from forms import ContactForm, FooterContactForm, LoginForm, UserAdminForm
from wtforms.fields import PasswordField
from flask.cli import with_appcontext
import click
from datetime import datetime
from sqlalchemy import text

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

@app.cli.command("fix-db-version")
@with_appcontext
def fix_db_version():
    """Manually sets the alembic_version in the database."""
    try:
        # Get the latest revision from the local migrations folder
        from alembic.script import ScriptDirectory
        from alembic.config import Config
        import os

        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", os.path.join(os.path.dirname(__file__), "migrations"))
        script = ScriptDirectory.from_config(alembic_cfg)
        head_revision = script.get_current_head()

        if not head_revision:
            click.echo("Error: Could not determine head revision from local migrations.")
            return

        # Execute raw SQL to update the alembic_version table
        db.session.execute(text(f"UPDATE alembic_version SET version_num = '{head_revision}'"))
        db.session.commit()
        click.echo(f"Successfully stamped alembic_version to {head_revision}.")
    except Exception as e:
        db.session.rollback()
        click.echo(f"Error fixing database version: {e}")

@app.cli.command("assign-role")
@click.argument("username")
@click.argument("role")
@with_appcontext
def assign_role(username, role):
    """Assigns a role to a user."""
    if role not in ['admin', 'editor']:
        click.echo(f"Error: Invalid role '{role}'. Must be 'admin' or 'editor'.")
        return

    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f"Error: User '{username}' not found.")
        return

    user.role = role
    db.session.commit()
    click.echo(f"Successfully assigned role '{role}' to user '{username}'.")

@app.cli.command("assign-role")
@click.argument("username")
@click.argument("role")
@with_appcontext
def assign_role(username, role):
    """Assigns a role to a user."""
    if role not in ['admin', 'editor']:
        click.echo(f"Error: Invalid role '{role}'. Must be 'admin' or 'editor'.")
        return

    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f"Error: User '{username}' not found.")
        return

    user.role = role
    db.session.commit()
    click.echo(f"Successfully assigned role '{role}' to user '{username}'.")

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

# Vista personalizada para el modelo User
class UserAdminView(SecuredModelView):
    # Usar el formulario personalizado
    form = UserAdminForm

    # Columnas a mostrar en la lista
    column_list = ('username', 'role')
    # No mostrar el hash en la lista de usuarios
    column_exclude_list = ('password_hash',)

    # Lógica de acceso
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # Redirigir si el usuario no es admin
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('admin.index'))

    # Hashear la contraseña nueva al guardar
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)

# Panel Admin
admin = Admin(app, name="Panel Admin", template_mode="bootstrap4", index_view=MyAdminIndexView())
admin.add_view(UserAdminView(User, db.session))
admin.add_view(SecuredModelView(SiteSetting, db.session))
admin.add_view(SecuredModelView(Service, db.session))
admin.add_view(SecuredModelView(Project, db.session))
admin.add_view(SecuredModelView(SuccessStory, db.session))
admin.add_view(SecuredModelView(ContactMessage, db.session))
admin.add_view(SecuredModelView(PopupMessage, db.session))
admin.add_link(MenuLink(name='Logout', url='/logout'))

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