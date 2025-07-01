from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from wtforms.validators import ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email ")])
    phone_region = StringField('phone region')
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    retype_password = PasswordField('retype Password', validators=[DataRequired()])
    walletType = StringField('Wallet Type', validators=[DataRequired()])
    ref_code = StringField("ref_code")
    walletAdress = StringField("Wallet Address", validators=[DataRequired()])
    submit = SubmitField('Register')


class ChangePsswordForm(FlaskForm):
    Currentpassword = PasswordField('Current Password', validators=[DataRequired()])
    NewPassword = PasswordField('New password', validators=[DataRequired()])
    ComfirmPassword = PasswordField('ComfirmPassword', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class ChangeWalletForm(FlaskForm):
    walletAdress = StringField("Wallet Address", validators=[DataRequired()])
    walletType = StringField('Wallet Type', validators=[DataRequired()])
    submit = SubmitField('Change Wallet Details')

class ChangePhoneAdmin(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    balance = StringField("Admin balnce", validators=[DataRequired()]) 
    phonew = StringField("Phone Whatsapp", validators=[DataRequired()])
    phonet = StringField('Phone Telegram', validators=[DataRequired()])
    submit = SubmitField('Change phone Details')


class ResetEmail(FlaskForm):
    inputbox = StringField("emall or phone", validators=[DataRequired()])
    submit = SubmitField('send')

class ResetPassword(FlaskForm):
    NewPassword = StringField("password", validators=[DataRequired()])
    otp = StringField('otp')
    submit = SubmitField('save')
    

