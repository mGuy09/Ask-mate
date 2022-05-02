from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_page():
    return render_template("list-page.html")


if __name__ == "__main__":
    app.run(debug=True)
