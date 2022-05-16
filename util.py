# from datetime import datetime
import os
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
# from data_manager
# from connection import rewrite_question_data, rewrite_answer_data
#
#
# def convert_time(time_in_millis):
#     dt = datetime.fromtimestamp(
#         float(time_in_millis) / 1000.0,
#     )
#     dt = dt.strftime("%d/%m/%Y  %H:%M")
#     return dt
#
#
# def get_time():
#     now = datetime.now()
#     now = now.strftime("%d/%m/%Y %H:%M:%S:%fff")
#     now = datetime.strptime(now, "%d/%m/%Y %H:%M:%S:%fff")
#     current_time = now.timestamp() * 1000


def delete_image(item, id):
    if item["id"] == int(id) and item['image'] != '<null>':
        os.remove(
            os.path.join(
                os.path.dirname(__file__),
                "static",
                "images",
                item["image"],
            )
        )


def upload_image():
    if request.files is not None:
        image = request.files["image"]
        path = os.path.join(
            os.path.dirname(__file__),
            "static",
            "images",
            secure_filename(image.filename),
        )
        image.save(path)
        return secure_filename(image.filename)
    return "<null>"

#
# def vote_question(data, id, modifier):
#     question_data = get_data(data)
#     for question in question_data:
#         if question["id"] == id:
#             question["vote_number"] = int(question["vote_number"]) + modifier
#
#     rewrite_question_data(data, question_data)
#     return redirect(url_for("list_page"))
#
#
# def vote_answer(data, id, modifier):
#     answer_data = get_data(data)
#     for answer in answer_data:
#         if answer["id"] == id:
#             answer["vote_number"] = int(answer["vote_number"]) + modifier
#             question_id = answer["question_id"]
#
#     rewrite_answer_data(data, answer_data)
#     return redirect(url_for("question", id=question_id))
