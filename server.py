from flask import Flask, render_template, request, redirect
import data_manager
import util
import os
import datetime
app = Flask(__name__)

questions = os.environ["QUESTION"]
answers = os.environ["ANSWER"]
'''
strs =  sorted(lista, key = lambda key: key['submission_time'])
'''


@app.route("/")
@app.route("/list")
def list_page():
    question_data = data_manager.get_data(questions)
    time = sorted(question_data, key = lambda i: i['submission_time'], reverse=True)
    for i in time:
        if i['submission_time'] != format('%d/%m/%Y  %H:%M'):
            i['submission_time'] = util.convert_time(i['submission_time'])
    return render_template("list-page.html", data=time)


@app.route('/question/<id>')
def question(id):
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



if __name__ == "__main__":
    app.run(debug=True)
