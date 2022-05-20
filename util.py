import os
from flask import request
from werkzeug.utils import secure_filename


def delete_image(item, id):
    if item["id"] == int(id) and item['image'] != '':
        os.remove(
            os.path.join(
                os.path.dirname(__file__),
                "static",
                "images",
                item["image"],
            )
        )


def upload_image():
    if request.files['image']:
        image = request.files["image"]
        path = os.path.join(
            os.path.dirname(__file__),
            "static",
            "images",
            secure_filename(image.filename),
        )
        image.save(path)
        return secure_filename(image.filename)
    return ''




