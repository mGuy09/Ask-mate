from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)
UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
@app.route("/list")
def list_page():
    return render_template("list-page.html", data=data_manager.get_data_question())


@app.route('/question/<id>',methods = ['POST','GET'])
def question(id):
    return render_template('question-page.html', question=data_manager.get_question(id), id=id)


@app.route('/add-question', methods=['GET','POST'])
def add_question():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        id = data_manager.add_question(title, message, image)
        return redirect(url_for('question',id=id))
    return render_template('add_question.html')


@app.route("/question/<id>/new-answer", methods=["GET", "POST"])
def add_answer(id):
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.add_data_answer(id, message)
        return redirect(url_for('question', id=id))
    return render_template('answer_question.html', id=id)



if __name__ == "__main__":
    app.run(debug=True)
