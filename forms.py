from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email

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
    submit = SubmitField('Enviar Mensaje')


class FooterContactForm(FlaskForm):
    # Lista de provincias de ejemplo
    provinces = [
        ('', 'Provincia...'),
        ('P1', 'Provincia 1'),
        ('P2', 'Provincia 2'),
        ('P3', 'Provincia 3'),
        ('P4', 'Provincia 4')
    ]

    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Teléfono')
    city = StringField('Ciudad')
    province = SelectField('Provincia', choices=provinces)
    comment = TextAreaField('Mensaje o Comentario')
    submit = SubmitField('Enviar')
