from flask import Flask, render_template, request, redirect
import data_manager
app = Flask(__name__)

'''
strs =  sorted(lista, key = lambda key: key['submission_time'])
'''

@app.route("/")
@app.route("/list")
def list_page():
    question_data = data_manager.questions_data
    time = sorted(question_data, key = lambda i: i['submission_time'])
    return render_template("list-page.html", data=time)


if __name__ == "__main__":
    app.run(debug=True)
