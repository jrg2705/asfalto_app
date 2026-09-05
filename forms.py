from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Optional, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ContactForm(FlaskForm):
    inquiry_choices = [
        ('', '¿Cómo podemos ayudarte?*'),
        ('quote', 'Solicitar una cotización'),
        ('support', 'Soporte de producto'),
        ('general', 'Consulta general'),
        ('career', 'Oportunidades de carrera')
    ]

    first_name = StringField('Nombre*', validators=[DataRequired()])
    last_name = StringField('Apellido*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    phone = StringField('Teléfono')
    company = StringField('Compañía')
    inquiry_type = SelectField('Tipo de consulta*', choices=inquiry_choices, validators=[DataRequired()])
    message = TextAreaField('Mensaje*', validators=[DataRequired()])
    # Honeypot anti-spam: los bots suelen rellenarlo, los humanos no lo ven
    website = HiddenField('Website')
    submit = SubmitField('Enviar Mensaje')

    def validate_website(self, field):
        if field.data:
            raise ValidationError('Spam detectado.')


class FooterContactForm(FlaskForm):
    provinces = [
        ('', 'Provincia...'),
        ('Azua', 'Azua'),
        ('Bahoruco', 'Bahoruco'),
        ('Barahona', 'Barahona'),
        ('Dajabón', 'Dajabón'),
        ('Distrito Nacional', 'Distrito Nacional'),
        ('Duarte', 'Duarte'),
        ('Elías Piña', 'Elías Piña'),
        ('El Seibo', 'El Seibo'),
        ('Espaillat', 'Espaillat'),
        ('Hato Mayor', 'Hato Mayor'),
        ('Hermanas Mirabal', 'Hermanas Mirabal'),
        ('Independencia', 'Independencia'),
        ('La Altagracia', 'La Altagracia'),
        ('La Romana', 'La Romana'),
        ('La Vega', 'La Vega'),
        ('María Trinidad Sánchez', 'María Trinidad Sánchez'),
        ('Monseñor Nouel', 'Monseñor Nouel'),
        ('Monte Cristi', 'Monte Cristi'),
        ('Monte Plata', 'Monte Plata'),
        ('Pedernales', 'Pedernales'),
        ('Peravia', 'Peravia'),
        ('Puerto Plata', 'Puerto Plata'),
        ('Samaná', 'Samaná'),
        ('Sánchez Ramírez', 'Sánchez Ramírez'),
        ('San Cristóbal', 'San Cristóbal'),
        ('San José de Ocoa', 'San José de Ocoa'),
        ('San Juan', 'San Juan'),
        ('San Pedro de Macorís', 'San Pedro de Macorís'),
        ('Santiago', 'Santiago'),
        ('Santiago Rodríguez', 'Santiago Rodríguez'),
        ('Santo Domingo', 'Santo Domingo'),
        ('Valverde', 'Valverde')
    ]

    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Teléfono')
    city = StringField('Ciudad')
    province = SelectField('Provincia', choices=provinces)
    comment = TextAreaField('Mensaje o Comentario')
    # Honeypot anti-spam
    website = HiddenField('Website')
    submit = SubmitField('Enviar')

    def validate_website(self, field):
        if field.data:
            raise ValidationError('Spam detectado.')


class UserAdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    role = SelectField('Role', choices=[('editor', 'Editor'), ('admin', 'Admin')], validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        Optional(),
        EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm New Password')
