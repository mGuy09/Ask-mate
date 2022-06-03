import flask

from bonus_questions import SAMPLE_QUESTIONS
from flask import Flask, render_template, request, redirect, url_for, session
import data_manager
import util
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)



@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/registration",methods = ['POST','GET'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = util.hash_password(password)
        data_manager.add_user(email,username,hashed_password)
        return redirect(url_for('login'))
    return render_template('registration.html')



@app.route("/")
def latest_questions():
    return render_template(
        "latest-page.html",
        data=data_manager.sort_question_data(
            request.args.get("sort", default="submission_time"),
            request.args.get("direction", default="desc"),
            5,
        )
    )


@app.route("/list")
def list_page():
    # if not session.get('logged_in'):
    #     return redirect(url_for('login'))
    return render_template(
        "list-page.html",
        data=data_manager.sort_question_data(
            request.args.get("sort", default="submission_time"),
            request.args.get("direction", default="desc"),
            "ALL"
        ), users=data_manager.get_all_users(), q_users=data_manager.get_all_question_user_id()
    )


@app.route("/question/<id>", methods=["POST", "GET"])
def question(id):
    data_manager.add_view(id)
    return render_template(
        "question-page.html",
        question=data_manager.get_question(id),
        answers=data_manager.get_data_answer(id),
        question_comments=data_manager.get_comment(id),
        answer_comment=data_manager.get_all_comments(),
        tags=data_manager.get_all_tags_by_question_id(id),
        id=id,
        accepted_answer=data_manager.get_user_id_question(id),
        answer_user_id=data_manager.get_all_answer_user_id()
    )


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if session:
        if request.method == "POST":
            question_id = data_manager.add_question(
                        request.form['title'],
                        request.form.get("message"),
                        util.upload_image(),
                        )
            data_manager.add_question_and_user(question_id,session['user_id'])
            return redirect(
                url_for(
                    "question",
                    id=question_id,


                )
            )
        return render_template("add_question.html")
    else:
        return redirect(url_for('login'))


@app.route("/question/<id>/new-answer", methods=["GET", "POST"])
def add_answer(id):
    if request.method == "POST":

        answer_id = data_manager.add_data_answer(
            id,
            request.form.get("message"),
            util.upload_image(),
        )
        data_manager.add_answer_and_user(answer_id,session['user_id'])
        return redirect(url_for("question", id=id))
    return render_template("answer_question.html", id=id)


@app.route("/question/<id>/delete")
def delete_question(id):
    util.delete_image(dict(data_manager.get_question(id)), id)
    for answer_id in data_manager.get_data_answer(id):
        comment_id = data_manager.delete_comment_by_answer_id(dict(answer_id)["id"])
        data_manager.delete_comment_from_user(comment_id)
        data_manager.delete_answer_from_user(answer_id)
    data_manager.delete_answers_by_question(id)
    data_manager.delete_tags_from_question(id)
    data_manager.delete_comment_by_question_id(id)
    data_manager.delete_question_id_from_user(id)
    data_manager.delete_data(id)
    return redirect(url_for("list_page"))


@app.route("/question/<id>/edit", methods=["POST", "GET"])
def update_question(id):
    if request.method == "POST":
        data_manager.update_data_question(
            id,
            request.form.get("title"),
            request.form.get("message"),
        )
        return redirect(url_for("question", id=id))
    return render_template(
        "edit_question.html",
        question=data_manager.get_question(id),
        id=id
    )


@app.route("/answer/<answer_id>/edit", methods=["POST", "GET"])
def update_answer(answer_id):
    if request.method == "POST":
        data_manager.update_data_answer(answer_id, request.form.get("message"))
        return redirect(
            url_for(
                "question",
                id=dict(data_manager.get_answer(answer_id))["question_id"],
            )
        )
    return render_template(
        "edit_answer.html",
        data=data_manager.get_answer(answer_id),
        id=answer_id
    )


def get_question_answer_ids(id):
    return (
        dict(data_manager.get_question_comment(id))["question_id"],
        dict(data_manager.get_question_comment(id))["answer_id"],
    )


@app.route("/comment/<comment_id>/edit", methods=["POST", "GET"])
def update_comment(comment_id):
    if request.method == "POST":
        data_manager.update_comments(comment_id, request.form.get("message"))
        question_id, answer_id = get_question_answer_ids(comment_id)
        if not question_id:
            question_id = dict(data_manager.get_answer(answer_id))["question_id"]
        return redirect(url_for("question", id=question_id))
    return render_template(
        "edit_comment.html",
        data=data_manager.get_question_comment(comment_id),
        id=comment_id
    )


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    data_manager.delete_answer_from_user(answer_id)
    util.delete_image(dict(data_manager.get_answer(answer_id)), answer_id)

    data_manager.delete_comment_by_answer_id(answer_id)
    return redirect(url_for("question", id=data_manager.delete_answer(answer_id)))


@app.route("/comment/<comment_id>/delete")
def delete_comment(comment_id):
    question_id, answer_id = get_question_answer_ids(comment_id)
    if not question_id:
        question_id = dict(data_manager.get_answer(answer_id))["question_id"]
    data_manager.delete_comment_from_user(comment_id)
    data_manager.delete_comment(comment_id)
    return redirect(url_for("question", id=question_id))


@app.route("/question/<id>/vote-up")
def vote_up(id):
    data_manager.vote_on_question(id, 1)
    user_id = data_manager.get_user_id_question(id)
    data_manager.add_rep(user_id.get('user_id'), 5)
    return redirect(url_for("list_page"))


@app.route("/question/<id>/vote-down")
def vote_down(id):
    data_manager.vote_on_question(id, -1)
    user_id = data_manager.get_user_id_question(id)
    data_manager.add_rep(user_id.get('user_id'), -2)
    return redirect(url_for("list_page"))


@app.route("/answer/<answer_id>/vote-up")
def vote_up_answer(answer_id):
    data_manager.vote_on_answer(answer_id, 1)
    user_id = data_manager.get_user_id_answer(answer_id)
    data_manager.add_rep(user_id.get('user_id'), 10)
    answer = dict(data_manager.get_answer(answer_id))
    return redirect(url_for("question", id=answer["question_id"]))


@app.route("/answer/<answer_id>/vote-down")
def vote_down_answer(answer_id):
    data_manager.vote_on_answer(answer_id, -1)
    user_id = data_manager.get_user_id_answer(answer_id)
    data_manager.add_rep(user_id.get('user_id'), -2)
    answer = dict(data_manager.get_answer(answer_id))
    return redirect(url_for("question", id=answer["question_id"]))


@app.route("/question/<id>/new-comment", methods=["GET", "POST"])
def add_comment(id):
    if request.method == "POST":

        comment_id = data_manager.add_comment(id, request.form.get("message"))
        data_manager.add_comment_and_user(comment_id,session['user_id'])
        return redirect(url_for("question", id=id))
    return render_template(
        "new-comment.html",
        id=id
    )


@app.route("/search")
def search_bar():
    selected_answers = []
    for question in data_manager.get_data_question():
        for answer in data_manager.search_answer(request.args.get("search_phrase")):
            if answer["question_id"] == question["id"]:
                selected_answers.append(question)

    return render_template(
        "search-list.html",
        data=data_manager.search_question(request.args.get("search_phrase")),
        answer_questions=selected_answers,
        search_phrase=request.args.get("search_phrase")
    )


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_answer(answer_id):
    if request.method == "POST":
        data_manager.add_comment_answer(answer_id, request.form.get("message"))
        return redirect(
            url_for(
                "question",
                id=data_manager.get_answer(answer_id).get("question_id", ""),
            )
        )
    return render_template("comment-answer.html", id=answer_id)


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def add_tag_to_question(question_id):
    error = False
    if request.method == "POST":
        new_tag = request.form.get("tag")
        all_tags = data_manager.get_tags()
        util.add_tag_to_db(all_tags, new_tag)
        for tag in data_manager.get_tags():
            if dict(tag)["name"] == new_tag:
                tag_id = dict(tag)["id"]
        if not data_manager.get_tag_from_question_tag(question_id, tag_id):
            data_manager.add_question_tag(question_id, tag_id)
            return redirect(url_for("question", id=question_id))
        else:
            error = True
    return render_template(
        "add_new_tag.html",
        tags=data_manager.get_tags(),
        question_id=question_id,
        error=error
    )


@app.get("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(tag_id, question_id)
    return redirect(url_for("question", id=question_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if data_manager.get_user(request.form['email_or_name']) is not None and util.verify_password(request.form['password'],
                                dict(data_manager.get_user(request.form['email_or_name']))['password']):

            session['logged_in'] = dict(data_manager.get_user(request.form['email_or_name']))['username']
            session['user_id'] = dict(data_manager.get_user(request.form['email_or_name']))['id']
            return redirect(url_for('list_page'))
        else:
            return render_template('login_page.html', error=True)
    return render_template('login_page.html', error=False)


@app.get('/logout')
def logout():
    session.clear()
    return redirect(url_for('latest_questions'))


@app.route('/users')
def users_page():
    return render_template('user_list.html',
                           users_info=data_manager.get_all_users(),
                           users_questions=data_manager.count_users_q(),
                           users_answers=data_manager.count_users_a(),
                           users_comments=data_manager.count_users_c())


@app.route('/user/<user_id>/<username>/', methods=['GET', 'POST'])
def get_user_page(user_id, username):
    if session:
        submission_time = data_manager.get_time(user_id)['registration_time']
        number_questions= data_manager.get_number_of_questions(user_id)[0]['count']
        number_answers = data_manager.get_number_of_answers(user_id)[0]['count']
        number_comments = data_manager.get_number_of_comments(user_id)[0]['count']
        questions = data_manager.get_questions(user_id)
        answers = data_manager.get_answers(user_id)
        comments = data_manager.get_comments(user_id)
        reputation = data_manager.get_reputation(user_id)['reputation']
        return render_template('user_page.html', id=user_id,
                               username=username,submission_time=submission_time,
                               number_questions=number_questions, number_answers=number_answers,
                               number_comments=number_comments, questions=questions,
                               answers=answers, comments=comments, reputation=reputation)
    else:
        return redirect(url_for('login'))


# @app.route('/bonus_questions', methods= ['POST', 'GET'])
# def get_bonus_questions():



@app.get('/show-answer/<answer_id>/<question_id>')
def show_answer(answer_id, question_id):
    data_manager.show_answer(answer_id)
    return redirect(url_for('question', id=question_id))


@app.get('/hide-answer/<answer_id>/<question_id>')
def hide_answer(answer_id, question_id):
    data_manager.hide_answer(answer_id)
    return redirect(url_for('question', id=question_id))


@app.get('/tags')
def tags_page():
    return render_template('tags_page.html', tags=data_manager.get_all_tags_from_questions())



if __name__ == "__main__":
    app.run(debug=True, port=5001)
