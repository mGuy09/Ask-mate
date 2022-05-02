from flask import Flask, render_template, request, redirect
import data_manager
import util
app = Flask(__name__)

'''
strs =  sorted(lista, key = lambda key: key['submission_time'])
'''

@app.route("/")
@app.route("/list")
def list_page():
    question_data = data_manager.questions_data
    time = sorted(question_data, key = lambda i: i['submission_time'])
<<<<<<< HEAD
    for i in time:
       i['submission_time'] = util.convert_time(i['submission_time'])


=======
>>>>>>> 68a424e35899e97ee0d3e57c47706ddda0b82900

    return render_template("list-page.html", data=time)


if __name__ == "__main__":
    app.run(debug=True)
