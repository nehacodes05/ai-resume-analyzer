from flask import Flask, render_template, request
from pypdf import PdfReader
from google import genai
import sqlite3
from dotenv import load_dotenv
import os

os.makedirs("uploads", exist_ok=True)

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
        if resume is None or resume.filename == "":
            return " Please upload a file"

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
        Analyse the following resume for the Target role

        Target Role:
        {target_role}
     
        Return plain text only.
        DO NOT use:
        **
        ###
        *
        -
        Markdown formatting

        Use this exact formatting:

        1.Resume score : X/10

        2.Missing Skills:

        -skill 1
        -skill 2
        -skill 3

        3.Improvement Suggestions:

        -Suggestion 1

        -Suggestion 2

        -Suggestion 3


        Resume:
        {text}
        """
        # send to gemini
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )

            # for saving analysis
            feedback = response.text

        except Exception as e:
            return render_template(
                "result.html",
                feedback="Gemini is currently busy.Please try again later",
            )

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


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
