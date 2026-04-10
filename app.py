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

        topic = request.form.get("topic")

        if not topic or topic.strip() == "":
            return "<h3>⚠️ Please enter a valid topic.</h3>"

        print("\nStarting research on:", topic)

        try:
            # -----------------------------
            # RUN RESEARCH
            # -----------------------------
            result = run_research(topic)

            research_data = result["research"]
            memory_context = result["memory"]
            error = result["error"]

            # Handle research error
            if error:
                return f"<h3>{error}</h3>"

            # -----------------------------
            # GENERATE REPORT
            # -----------------------------
            report = generate_report(research_data, memory_context, topic)

            # Handle report error
            if not report or "⚠️" in report:
                return "<h3>⚠️ Failed to generate report.</h3>"

            # -----------------------------
            # SAVE REPORT
            # -----------------------------
            filename = topic.replace(" ", "_").lower() + ".txt"
            filepath = os.path.join("reports", filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)

            return f"<pre>{report}</pre>"

        except Exception as e:
            print("🔥 ERROR:", e)
            return "<h3>⚠️ Server is busy. Please try again.</h3>"

    return render_template("index.html")


# -----------------------------
# Research History Page
# -----------------------------
@app.route("/history")
def history():

    try:
        reports = os.listdir("reports")
    except:
        reports = []

    return render_template("history.html", reports=reports)


# -----------------------------
# Open Saved Report
# -----------------------------
@app.route("/reports/<filename>")
def get_report(filename):

    try:
        filepath = os.path.join("reports", filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        return f"<pre>{content}</pre>"

    except:
        return "<h3>⚠️ Report not found.</h3>"


if __name__ == "__main__":
    app.run(debug=True)