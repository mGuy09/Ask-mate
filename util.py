import os
from flask import request
from werkzeug.utils import secure_filename
import data_manager


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


def add_tag_to_db(all_tags, new_tag):
    for tag in all_tags:
        if dict(tag)["name"] == new_tag:
            break
    else:
        data_manager.add_new_tag(new_tag)

