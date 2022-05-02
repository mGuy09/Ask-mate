from flask import Flask, render_template, request, redirect
import data_manager
app = Flask(__name__)



@app.route("/")
@app.route("/list")
def list_page():
    question_data = data_manager.questions_data
    return render_template("list-page.html", data=question_data)


if __name__ == "__main__":
    app.run(debug=True)
