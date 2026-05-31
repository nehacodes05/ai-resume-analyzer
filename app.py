from flask import Flask, render_template, request
from pypdf import PdfReader
from google import genai
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("resume.db")

    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          target_role TEXT,
          resume_text TEXT,
          Feedback TEXT,
          upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
                                                 
    """)
    conn.commit()
    conn.close()


# Gemini API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # get uploaded files
        resume = request.files.get("resume")
        # get target role
        target_role = request.form.get("target_role")

        feedback = "GOOD RESUME"

        # validating
        if resume.filename == "":
            return " please upload a file"

        # save file
        filepath = f"uploads/{resume.filename}"
        resume.save(filepath)  # physically creates files in upload folder

        # extract text
        reader = PdfReader(filepath)  # open pdf & creates a pdf reader object
        text = ""  # create empty txt to store extracted text

        for page in reader.pages:
            text += page.extract_text()  # += add new txt to existing txt

        # validating after extraction
        if text.strip() == "":
            return "no readable text found in PDF"

        # PROMPT
        prompt = f"""
        Analyse the following resume.

        Target Role:
        {target_role}

        Give:
        1. Resume Score out of 10
        2.Missing Skills
        3.Improvement Suggestions

        Resume:
        {text}
        """
        # send to gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        # for saving analysis
        feedback = response.text

        conn = sqlite3.connect("resume.db")

        cursor = conn.cursor()

        cursor.execute(
            """
        INSERT INTO analysis
        (target_role,resume_text,feedback)
        VALUES(?,?,?)
        """,
            (target_role, text, feedback),
        )

        conn.commit()
        conn.close()

        # nice result page
        return render_template("result.html", feedback=feedback)
    return render_template("index.html")


# analysis history
@app.route("/history")
def history():
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id,
            target_role,
            upload_date
    FROM analysis
    ORDER BY id DESC
    
    """)
    records = cursor.fetchall()
    conn.close()

    return render_template("history.html", records=records)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
