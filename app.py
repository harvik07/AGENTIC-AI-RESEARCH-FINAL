from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from research_engine import run_research
from generate_report import generate_report

# load environment variables
load_dotenv()

app = Flask(__name__)

# ensure reports folder exists
os.makedirs("reports", exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        topic = request.form["topic"]

        print("\nStarting research on:", topic)

        # run research pipeline
        research_data = run_research(topic)

        # generate report
        report = generate_report(topic, research_data)

        # create safe filename
        filename = topic.replace(" ", "_").lower() + ".txt"

        filepath = os.path.join("reports", filename)

        # save report
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)

        return f"<pre>{report}</pre>"

    return render_template("index.html")


# -----------------------------
# Research History Page
# -----------------------------
@app.route("/history")
def history():

    reports = os.listdir("reports")

    return render_template("history.html", reports=reports)


# -----------------------------
# Open Saved Report
# -----------------------------
@app.route("/reports/<filename>")
def get_report(filename):

    filepath = os.path.join("reports", filename)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    return f"<pre>{content}</pre>"


if __name__ == "__main__":
    app.run(debug=True)