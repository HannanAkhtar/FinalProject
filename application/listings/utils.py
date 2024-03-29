import os
import secrets
from flask import current_app
from PIL import Image


def save_listing_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/listings_pics', picture_fn)

    i = Image.open(form_picture)
    if i.mode in ("RGBA", "P"): i = i.convert("RGB")
    i.save(picture_path)

    return picture_fn