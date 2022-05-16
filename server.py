from flask import Flask, render_template, request, redirect, url_for
import data_manager
import util

app = Flask(__name__)
UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
@app.route("/list")
def list_page():
    sorting = request.args.get('sort',default='submission_time')
    direction = request.args.get('direction', default='desc')
    question_data = data_manager.sort_question_data(sorting,direction)

    return render_template("list-page.html", data=question_data)


@app.route('/question/<id>',methods = ['POST','GET'])
def question(id):
    return render_template('question-page.html', question=data_manager.get_question(id), id=id)


@app.route('/add-question', methods=['GET','POST'])
def add_question():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        image = util.upload_image()
        id = data_manager.add_question(title, message, image)
        return redirect(url_for('question',id=id))
    return render_template('add_question.html')


@app.route("/question/<id>/new-answer", methods=["GET", "POST"])
def add_answer(id):
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.add_data_answer(id, message, util.upload_image())
        return redirect(url_for('question', id=id))
    return render_template('answer_question.html', id=id)


@app.route("/question/<id>/delete")
def delete_question(id):
    util.delete_image(dict(data_manager.get_question(id)), id)
    data_manager.delete_data(id)

    return redirect(url_for('list_page'))


@app.route('/question/<id>/edit', methods= ['POST','GET'])
def update_question(id):
    question = data_manager.get_question(id)
    current = question



    if request.method == 'POST':

        title = request.form.get("title")
        message = request.form.get("message")
        data_manager.update_data_question(id, title, message)
        return redirect(url_for('question',id=id))
    return render_template('edit_question.html', question=current, id=id)



if __name__ == "__main__":
    app.run(debug=True)
