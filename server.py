from flask import Flask, render_template, request, redirect,url_for
import data_manager
import util
import os
from werkzeug.utils import secure_filename
import connection
app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

questions = os.environ["QUESTION"]
answers = os.environ["ANSWER"]


@app.route("/")
@app.route("/list", methods=["GET"])
def list_page():
    sorting = request.args.get("sort", default='submission_time')
    direction = request.args.get("direction", default=True)

    question_data = data_manager.sort_asc(questions, sorting, direction)

    return render_template("list-page.html", data=question_data)


@app.route('/question/<id>', methods=['GET'])
def question(id):
    question_dict = {}
    question_data = data_manager.get_data(questions)
    answer_data = data_manager.get_data(answers)
    time = sorted(answer_data, key=lambda i: i['submission_time'], reverse=True)
    answer_list = []
    for question in question_data:
        if question['id'] == id:
            if request.method == "GET":
                question['view_number'] = int(question['view_number']) + 1
            question_dict = question
            for answer in time:
                if answer['submission_time'] != format('%d/%m/%Y %H:%M'):
                    answer['submission_time'] = util.convert_time(answer['submission_time'])
                if id == answer['question_id']:
                    answer_list.append(answer)

    connection.rewrite_question_data(questions, question_data)
    return render_template('question-page.html',
                           answer_list=answer_list,
                           question_dict=question_dict,
                           id=id)


@app.route('/question/<id>/delete')
def delete_question(id):
    question = data_manager.get_data(questions)
    answer_list = data_manager.get_data(answers)
    deleting_answer_list = []
    for i in question:
        if i["id"] == id:
            path = os.path.join(os.path.dirname(__file__), 'static', 'images', i["image"])

    position_of_last_slash = path.rfind('/')
    if path[position_of_last_slash + 1:] == '':
        path = ''
    else:
        os.remove(path)
    for i in answer_list:
        if i["question_id"] == id:
            deleting_answer_list.append(i)
    for i in deleting_answer_list:
        data_manager.remove_answer(answers, i["id"])
    data_manager.remove_question(questions, id)
    return redirect(url_for('list_page'))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answer_list = data_manager.get_data(answers)
    for i in answer_list:
        if i["id"] == answer_id:
            path = os.path.join(os.path.dirname(__file__), 'static', 'images', i["image"])
            position_of_last_slash = path.rfind('/')
            if path[position_of_last_slash + 1:] == '':
                path = ''
            else:
                os.remove(path)
    question_id = data_manager.remove_answer(answers, answer_id)
    return redirect(url_for('question', id=question_id))


@app.route("/add-question", methods=["GET", "POST"])
def add_question_page():
    new_id = connection.get_new_id(questions)
    current_time = util.get_time()
    if request.method == 'POST':
        if len(request.files):
            image = request.files['image']
            path = os.path.join(os.path.dirname(__file__),'static','images',secure_filename(image.filename))
            position_of_last_slash = path.rfind('/')
            if path[position_of_last_slash+1:] == '':
                path = ''
            else:
                image.save(path)
            connection.append_data(questions,
                               {
                                   'id': new_id,
                                   'submission_time': current_time,
                                   'view_number': "0",
                                   'vote_number': "0",
                                   'title': request.form.get('title'),
                                   'message': request.form.get('message'),
                                   'image': path[position_of_last_slash+1:]
                               })

        return redirect(url_for('question',id=new_id))
    return render_template('add_question.html')


@app.route('/question/<id>/new-answer', methods=["GET", "POST"])
def add_answer(id):
    new_id = connection.get_new_id(answers)
    current_time = util.get_time()
    question_data = data_manager.get_data(questions)
    question_dict={}
    for question in question_data:
        if question['id'] == id:
            question_dict = question
            if request.method == 'POST':
                image = request.files['image']
                path = os.path.join(os.path.dirname(__file__), 'static', 'images', secure_filename(image.filename))
                position_of_last_slash = path.rfind('/')
                if path[position_of_last_slash + 1:] == '':
                    path = ''
                else:
                    image.save(path)
                connection.append_answer(answers, {
                    'id': new_id,
                    'submission_time': current_time,
                    'vote_number': '0',
                    'question_id': id,
                    'message': request.form.get('message'),
                    'image': path[position_of_last_slash+1:]
                })
                return redirect(url_for('question', id=id))
    return render_template("answer_question.html", id=id, question_dict=question_dict)


@app.route('/question/<id>/edit',methods = ['POST','GET'])
def update_question(id):
    question_data = data_manager.get_data(questions)
    current = [question for question in question_data if question.get('id') == id][0]
    current_time = util.get_time()


    if request.method == 'POST':
        # current['title'] = request.form.get('title')
        # current['message'] = request.form.get('message')

        # for index, row in enumerate(question_data):
        #     if row['id'] == id:
        #         question_data[index] = current

        for question in question_data:
            if question['id'] == id:
                question['title'] = request.form.get('title')
                question['message'] = request.form.get('message')
                question['submission_time'] = current_time
        connection.rewrite_question_data(questions,question_data)

        return redirect(url_for('question',id = id))

    return render_template('edit_question.html', result= current)


@app.route('/question/<id>/vote-up')
def vote_up(id):
    question_data = data_manager.get_data(questions)
    #current = [question for question in question_data if question.get('id') == id][0]

    if request.method == 'GET':
        for question in question_data:
            if question['id'] == id:
                question['vote_number'] = int(question['vote_number']) + 1

        connection.rewrite_question_data(questions,question_data)

    return redirect(url_for('list_page'))


@app.route('/question/<id>/vote-down')
def vote_down(id):
    question_data = data_manager.get_data(questions)
    if request.method == 'GET':
        for question in question_data:
            if question['id'] == id:
                question['vote_number'] = int(question['vote_number']) - 1

        connection.rewrite_question_data(questions,question_data)

    return redirect(url_for('list_page'))


@app.route('/answer/<answer_id>/vote-up')
def answer_vote_up(answer_id):
    answer_data = data_manager.get_data(answers)
    if request.method == 'GET':
        for answer in answer_data:
            if answer['id'] == answer_id:
                answer['vote_number'] = int(answer['vote_number']) + 1
                question_id = answer['question_id']

        connection.rewrite_answer_data(answers, answer_data)
    return redirect(url_for('question', id=question_id))


@app.route('/answer/<answer_id>/vote-down')
def answer_vote_down():
    pass


if __name__ == "__main__":
    app.run(debug=True)
