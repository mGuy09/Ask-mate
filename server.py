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


if __name__ == "__main__":
    app.run(debug=True)
