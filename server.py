from flask import Flask, render_template, request, redirect
import connection
app = Flask(__name__)

question = connection.read_question('question.csv')
answer = connection.read_question('answer.csv')


@app.route("/")
@app.route("/list")
def list_page():

    return render_template("list-page.html")


if __name__ == "__main__":
    app.run(debug=True)
