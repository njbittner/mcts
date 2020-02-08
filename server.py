from flask import Flask, render_template
import os

app = Flask(__name__, static_url_path=os.path.dirname(__file__))


@app.route("/chartjs")
def chartjs():
    return render_template("index2.html")
@app.route("/plotly")
def plotly():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
