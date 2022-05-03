from flask import Flask, render_template, request, redirect,url_for
import data_manager
import util
import os
import connection
app = Flask(__name__)

questions = os.environ["QUESTION"]
answers = os.environ["ANSWER"]
'''
strs =  sorted(lista, key = lambda key: key['submission_time'])
'''


@app.route("/")
@app.route("/list", methods=["GET"])
def list_page():
    sorting = request.args.get("sort", default='submission_time')
    direction = request.args.get("direction", default=False)

    question_data = data_manager.sort_asc(questions, sorting, direction)

    return render_template("list-page.html", data=question_data)



@app.route('/question/<id>')
def question(id):
    question_dict ={}
    question_data = data_manager.get_data(questions)
    answer_data = data_manager.get_data(answers)
    time = sorted(answer_data, key=lambda i: i['submission_time'], reverse=True)
    answer_list = []
    for question in question_data:
        if question['id'] == id:
            question_dict = question
            for answer in time:
                if answer['submission_time'] != format('%d/%m/%Y %H:%M'):
                    answer['submission_time'] = util.convert_time(answer['submission_time'])
                if id == answer['question_id']:
                    answer_list.append(answer)

    return render_template('question-page.html',
                           answer_list = answer_list,
                           question_dict = question_dict,
                           id=id)


@app.route('/question/<id>/delete')
def delete_question(id):
    data_manager.remove_question(questions, id)

    return redirect(url_for('list_page'))


@app.route("/add-question", methods=["GET", "POST"])
def add_question_page():
    new_id = connection.get_new_id(questions)
    current_time = util.get_time()
    if request.method == 'POST':
        connection.append_data(questions,
                               {
                'id':new_id,
                'submission_time':current_time,
                'view_number': "0",
                'vote_number': "0",
                'title': request.form.get('title'),
                'message': request.form.get('message'),
            })

        return redirect(url_for('question',id=new_id))

    return render_template('add_question.html')


@app.route('/question/<id>/new-answer', methods=["GET", "POST"])
def add_answer(id):
    new_id = connection.get_new_id(questions)
    current_time = util.get_time()
    question_data = data_manager.get_data(questions)
    question_dict={}
    for question in question_data:
        if question['id'] == id:
            question_dict = question
            if request.method == 'POST':
                connection.append_answer(answers,{
                    'id': new_id,
                    'submission_time': current_time,
                    'vote_number': '0',
                    'question_id': id,
                    'message': request.form.get('message')
                })
                return redirect(url_for('question', id=id))
    return render_template("answer_question.html", id=id, question_dict=question_dict)


if __name__ == "__main__":
    app.run(debug=True)
