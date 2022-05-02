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
    time = sorted(question_data, key = lambda i: i['submission_time'])
    for i in time:
        if i['submission_time'] != format('%d/%m/%Y  %H:%M'):
            i['submission_time'] = util.convert_time(i['submission_time'])
    return render_template("list-page.html", data=time)



@app.route('/question/<id>')
def question(id):
    question_data = data_manager.get_data(questions)
    answer_data = data_manager.get_data(answers)
    answer_list = []
    question_list = []
    for question in question_data:
        if question['id'] == id:
            title = question['title']
            message = question['message']
            question_list.append(title)
            question_list.append(message)
            for answer in answer_data:
                if id  == answer['question_id']:
                    answer_list.append(answer)


            return render_template('question-page.html', answer_list=answer_list,question_list=question_list)



if __name__ == "__main__":
    app.run(debug=True)
