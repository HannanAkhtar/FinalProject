import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from application import mail


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
    msg = Message('Password Reset Request', sender='yakeem.app@gmail.com', recipients=[user.email])
    msg.body = f'''Please visit the following link to reset your password:
{url_for('users.reset_token', token=token, _external=True)}

If you have not requested a password reset simply ignore this message.

Sincerely,
The Yakeem Team
'''

    mail.send(msg)