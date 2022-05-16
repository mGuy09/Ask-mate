from flask import Flask, render_template, request, redirect, url_for
import data_manager
import util

app = Flask(__name__)
UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
@app.route("/list")
def list_page():
    return render_template("list-page.html", data=data_manager.sort_question_data(request.args.get('sort',default='submission_time'),request.args.get('direction', default='desc')))


@app.route('/question/<id>',methods = ['POST','GET'])
def question(id):
    return render_template('question-page.html', question=data_manager.get_question(id),answers=data_manager.get_data_answer(id), id=id)


@app.route('/add-question', methods=['GET','POST'])
def add_question():
    if request.method == 'POST':
        return redirect(url_for('question',id=data_manager.add_question(request.form.get('title'), request.form.get('message'), util.upload_image())))
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


@app.route('/question/<id>/edit', methods= ['POST','GET'])
def update_question(id):
    if request.method == 'POST':
        data_manager.update_data_question(id, request.form.get("title"), request.form.get("message"))
        return redirect(url_for('question',id=id))
    return render_template('edit_question.html', question=data_manager.get_question(id), id=id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    util.delete_image(dict(data_manager.get_answer(answer_id)), answer_id)

    return redirect(url_for('question', id=data_manager.delete_answer(answer_id)))


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


if __name__ == "__main__":
    app.run(debug=True)
