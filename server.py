from flask import Flask, render_template, request, redirect, url_for
import data_manager
import util
import os
import connection

app = Flask(__name__)
UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
#
# questions = os.environ["QUESTION"]
# answers = os.environ["ANSWER"]


@app.route("/")
@app.route("/list")
def list_page():
    question_data = data_manager.get_data()
    # sorting = request.args.get("sort", default="submission_time")
    # direction = request.args.get("direction", default=True)

    # question_data = data_manager.sort_asc(questions, sorting, direction)

    return render_template("list-page.html", data=question_data)


@app.get('/question/<id>')
def question(id):
    return render_template('question-page.html', question=data_manager.get_question(id), id=id)


@app.route('/add-question', methods=['GET','POST'])
def add_question():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        id = data_manager.add_question(title, message, image)
        return redirect(url_for(question, id=id))
    return render_template('add_question.html')

# @app.route("/question/<id>")
# def question(id):
#     question_dict = {}
#     question_data = data_manager.get_data(questions)
#     sorted_answers = sorted(
#         data_manager.get_data(answers),
#         key=lambda i: i["submission_time"],
#         reverse=True,
#     )
#     answer_list = []
#
#     for question in question_data:
#         if question["id"] == id:
#             question["view_number"] = int(question["view_number"]) + 1
#             question_dict = question
#             for answer in sorted_answers:
#                 if answer["submission_time"] != format("%d/%m/%Y %H:%M"):
#                     answer["submission_time"] = util.convert_time(
#                         answer["submission_time"]
#                     )
#                 if id == answer["question_id"]:
#                     answer_list.append(answer)
#
#     connection.rewrite_question_data(questions, question_data)
#     return render_template(
#         "question-page.html",
#         answer_list=answer_list,
#         question_dict=question_dict,
#         id=id,
#     )
#
#
# @app.route("/question/<id>/delete")
# def delete_question(id):
#     question = data_manager.get_data(questions)
#     answer_list = data_manager.get_data(answers)
#
#     for i in question:
#         util.delete_image(i, id)
#
#     for i in answer_list:
#         if i["question_id"] == id:
#             data_manager.remove_answer(answers, i["id"])
#
#     data_manager.remove_question(questions, id)
#     return redirect(url_for("list_page"))
#
#
# @app.route("/answer/<answer_id>/delete")
# def delete_answer(answer_id):
#     answer_list = data_manager.get_data(answers)
#     for i in answer_list:
#         util.delete_image(i, answer_id)
#
#     question_id = data_manager.remove_answer(answers, answer_id)
#     return redirect(url_for("question", id=question_id))
#
#
# @app.route("/add-question", methods=["GET", "POST"])
# def add_question_page():
#     new_id = connection.get_new_id(questions)
#
#     if request.method == "POST":
#         connection.append_data(
#             questions,
#             {
#                 "id": new_id,
#                 "submission_time": util.get_time(),
#                 "view_number": "0",
#                 "vote_number": "0",
#                 "title": request.form.get("title"),
#                 "message": request.form.get("message"),
#                 "image": util.upload_image(),
#             },
#         )
#
#         return redirect(url_for("question", id=new_id))
#     return render_template("add_question.html")
#
#
# @app.route("/question/<id>/new-answer", methods=["GET", "POST"])
# def add_answer(id):
#     question_dict = {}
#
#     for question in data_manager.get_data(questions):
#         if question["id"] == id:
#             question_dict = question
#
#     if request.method == "POST":
#         connection.append_answer(
#             answers,
#             {
#                 "id": connection.get_new_id(answers),
#                 "submission_time": util.get_time(),
#                 "vote_number": "0",
#                 "question_id": id,
#                 "message": request.form.get("message"),
#                 "image": util.upload_image(),
#             },
#         )
#         return redirect(url_for("question", id=id))
#
#     return render_template("answer_question.html", id=id, question_dict=question_dict)
#
#
# @app.route("/question/<id>/edit", methods=["POST", "GET"])
# def update_question(id):
#     question_data = data_manager.get_data(questions)
#     current = [question for question in question_data if question.get("id") == id][0]
#
#     if request.method == "POST":
#         for question in question_data:
#             if question["id"] == id:
#                 question["title"] = request.form.get("title")
#                 question["message"] = request.form.get("message")
#                 question["submission_time"] = util.get_time()
#
#         connection.rewrite_question_data(questions, question_data)
#         return redirect(url_for("question", id=id))
#
#     return render_template("edit_question.html", result=current)
#
#
# @app.route("/question/<id>/vote-up")
# def vote_up(id):
#     return util.vote_question(questions, id, 1)
#
#
# @app.route("/question/<id>/vote-down")
# def vote_down(id):
#     return util.vote_question(questions, id, -1)
#
#
# @app.route("/answer/<answer_id>/vote-up")
# def answer_vote_up(answer_id):
#     return util.vote_answer(answers, answer_id, 1)
#
#
# @app.route("/answer/<answer_id>/vote-down")
# def answer_vote_down(answer_id):
#     return util.vote_answer(answers, answer_id, -1)
#

if __name__ == "__main__":
    app.run(debug=True)
