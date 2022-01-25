from flask_mail import Message
import os
import secrets
from PIL import Image
from flask import current_app, url_for
from rankTheBoysApp import mail, db
from rankTheBoysApp.models import User

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn   

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                sender='mikecatanidev@gmail.com',
                recipients = [user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token = token, _external=True)}

If you did not make this request, then simply ignore this email and no changes
will be made.'''
    mail.send(msg)

def calculateEloAmount(winner: User, loser: User):
        kFactor = 32
        winnerExpectedScore = 1 / (1 + pow(10, (loser.rating - winner.rating)/400))
        loserExpectedScore = 1/ (1 + pow(10, (winner.rating - loser.rating)/400))

        winner.rating = winner.rating + kFactor*(1 - winnerExpectedScore)
        loser.rating = loser.rating + kFactor*(0 - loserExpectedScore)
        db.session.commit()