from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField

class UserForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    password2 = PasswordField('Password')
    submit = SubmitField('Kaydet')

class KullaniciSil(FlaskForm):
    selectbox = SelectField()
    submit = SubmitField('Sil')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Giriş Yap')

class PlakaEkle(FlaskForm):
    plaka = StringField('Plaka')
    name = StringField('Name')
    surname = StringField('Surname')
    submit = SubmitField('Kaydet')

class PlakaSil(FlaskForm):
    selectbox = SelectField()
    submit = SubmitField('Sil')



