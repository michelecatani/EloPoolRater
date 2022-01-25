from ast import Pass
from wsgiref.validate import validator
from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from rankTheBoysApp.models import User

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    ## ensuring that we don't have multiple users with same name
    def validate_username(self, username):
        ## if there is a value, it'll be here. if not, it will jsut return none
        user = User.query.filter_by(username=username.data).first()
        ## if user is none, won't hit this conditional
        if user:
            raise ValidationError('That username is taken! Please choose another one.')

    ## ensuring that we don't have multiple users with same email
    def validate_email(self, email):
        ## if there is a value, it'll be here. if not, it will jsut return none
        email = User.query.filter_by(email=email.data).first()
        ## if email is none, won't hit this conditional
        if email:
            raise ValidationError('That email is taken! Please choose another one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember me')
    submit = SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    ## DataRequired() means we need this field (obviously), length is for the min and max(obviously)
    email = StringField('Email', validators=[DataRequired(), Email()])
    ## email will check if its equal to a correct email 
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit= SubmitField('Update')

    ## ensuring that we don't have multiple users with same name
    def validate_username(self, username):
        ## if there is a value, it'll be here. if not, it will jsut return none
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            ## if user is none, won't hit this conditional
            if user:
                raise ValidationError('That username is taken! Please choose another one.')

    ## ensuring that we don't have multiple users with same email
    def validate_email(self, email):
        ## if there is a value, it'll be here. if not, it will jsut return none
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            ## if email is none, won't hit this conditional
            if email:
                raise ValidationError('That email is taken! Please choose another one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user == None:
            raise ValidationError('There is no account with that email. You must be registered.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class MatchForm(FlaskForm):
    whoYouPlayed = StringField('Opponent', validators=[DataRequired()])
    didYouWin = BooleanField('Did you win?')
    submit = SubmitField('Log Match')

    def validate_opponent(self, whoYouPlayed):
        user = User.query.filter_by(username=whoYouPlayed.data).first()
        if user == None:
            raise ValidationError('There is no account with that username.')
        if user == current_user:
            raise ValidationError('You cannot play yourself!')