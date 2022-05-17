from flask import Flask, render_template, request, redirect, url_for
import data_manager
import util
import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def latest_questions():
    return render_template("latest-page.html",
                           data=data_manager.sort_question_data(request.args.get('sort', default='submission_time'),
                                                                request.args.get('direction', default='desc'),
                                                                5))


@app.route("/list")
def list_page():
    return render_template("list-page.html",
                           data=data_manager.sort_question_data(request.args.get('sort', default='submission_time'),
                                                                request.args.get('direction', default='desc'),
                                                                'ALL'))


@app.route('/question/<id>', methods=['POST', 'GET'])
def question(id):
    # answers = data_manager.get_data_answer(id)
    # answer_comment_list = []
    # for answer in answers:
    #     good_answer = data_manager.get_comment_answer(answer.get('id'))
    #     for elem in good_answer:
    #         answer_comment_list.append(elem
    #             # 'message': elem.get('message'),
    #             # 'submission_time': elem.get('submission_time')
    #         )
    # lista=[]
    # for i in answer_comment_list:
    #     # lista.append(i.get('submission_time'))
    #     lista.append(i.get('message'))
    # print(lista)
    answer_comment = data_manager.get_all_comments()
    return render_template('question-page.html',
                           question=data_manager.get_question(id),
                           answers=data_manager.get_data_answer(id),
                           question_comments=data_manager.get_comment(id),
                           answer_comment= answer_comment, id=id)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        return redirect(url_for('question',
                                id=data_manager.add_question(request.form.get('title'), request.form.get('message'),
                                                             util.upload_image())))
    return render_template('add_question.html')


@app.route("/question/<id>/new-answer", methods=["GET", "POST"])
def add_answer(id):
    if request.method == 'POST':
        data_manager.add_data_answer(id, request.form.get('message'), util.upload_image())
        return redirect(url_for('question', id=id))
    return render_template('answer_question.html', id=id)


@app.route("/question/<id>/delete")
def delete_question(id):
    util.delete_image(dict(data_manager.get_question(id)), id)
    data_manager.delete_answers_by_question(id)
    data_manager.delete_data(id)
    return redirect(url_for('list_page'))


@app.route('/question/<id>/edit', methods=['POST', 'GET'])
def update_question(id):
    if request.method == 'POST':
        data_manager.update_data_question(id, request.form.get("title"), request.form.get("message"))
        return redirect(url_for('question', id=id))
    return render_template('edit_question.html', question=data_manager.get_question(id), id=id)


@app.route('/answer/<answer_id>/edit', methods=['POST', 'GET'])
def update_answer(answer_id):
    if request.method == 'POST':
        data_manager.update_data_answer(answer_id, request.form.get('message'))
        return redirect(url_for('question', id=dict(data_manager.get_answer(answer_id))['question_id']))
    return render_template('edit_answer.html', data=data_manager.get_answer(answer_id), id=answer_id)


@app.route('/comment/<comment_id>/edit', methods=['POST', 'GET'])
def update_comment(comment_id):
    if request.method == 'POST':
        data_manager.update_comments(comment_id, request.form.get('message'))
        return redirect(url_for('question', id=dict(data_manager.get_question_comment(comment_id))['question_id']))
    return render_template('edit_comment.html', data=data_manager.get_question_comment(comment_id), id=comment_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    util.delete_image(dict(data_manager.get_answer(answer_id)), answer_id)

    return redirect(url_for('question', id=data_manager.delete_answer(answer_id)))


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    return redirect(url_for('question', id=data_manager.delete_comment(comment_id)))


@app.route('/question/<id>/vote-up')
def vote_up(id):
    data_manager.vote_on_question(id, 1)
    return redirect(url_for('list_page'))


@app.route('/question/<id>/vote-down')
def vote_down(id):
    data_manager.vote_on_question(id, -1)
    return redirect(url_for('list_page'))


@app.route('/answer/<answer_id>/vote-up')
def vote_up_answer(answer_id):
    data_manager.vote_on_answer(answer_id, 1)
    answer = dict(data_manager.get_answer(answer_id))
    return redirect(url_for('question', id=answer['question_id']))


@app.route('/answer/<answer_id>/vote-down')
def vote_down_answer(answer_id):
    data_manager.vote_on_answer(answer_id, -1)
    answer = dict(data_manager.get_answer(answer_id))
    return redirect(url_for('question', id=answer['question_id']))


@app.route('/question/<id>/new-comment', methods=['GET', 'POST'])
def add_comment(id):
    if request.method == 'POST':
        data_manager.add_comment(id, request.form.get('message'))
        return redirect(url_for('question', id=id))
    return render_template('new-comment.html', id=id, )


@app.route('/search')
def search_bar():
    search_phrase = request.args.get('search_phrase')
    all_questions = data_manager.get_data_question()
    search_answers = data_manager.search_answer(request.args.get(search_phrase))
    selected_answers = []
    for question in all_questions:
        for answer in search_answers:
            if dict(answer)['question_id'] == dict(question)['id']:
                selected_answers.append(question)

    return render_template('search-list.html',
                           data=data_manager.search_question(request.args.get('search_phrase')),
                           answer_questions=selected_answers, search_phrase=search_phrase)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    if request.method == 'POST':
        answer = data_manager.get_answer(answer_id)
        message= request.form.get('message')
        # submission_time = datetime.now()
        data_manager.add_comment_answer(answer_id, message)
        answers=data_manager.get_answer(answer_id)
        question_id = answers.get('question_id','')
        return redirect(url_for('question', id=question_id))
    return render_template('comment-answer.html', id=answer_id)

@app.route('/question/<question_id>/new-tag', methods = ['POST'])
def add_tag_to_question(question_id):
    tags = data_manager.get_tags()
    if request.method == 'POST':
        tag_id = request.form.get('tag_id')
        data_manager.add_question_tags(question_id, tag_id )
        return redirect(url_for('question', id=question_id))
    return render_template('tags.html', tags=tags)



if __name__ == "__main__":
    app.run(debug=True)
