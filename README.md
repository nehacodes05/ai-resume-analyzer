# AI Resume Analyzer

An AI-powered web application that analyzes PDF resumes against a target job role using Google's Gemini AI. The application extracts text from uploaded resumes, evaluates them based on the selected role, identifies missing skills, provides improvement suggestions, and stores analysis history for future reference.



## Features

- Upload resumes in PDF format
- Extract text automatically using PyPDF
- Analyze resumes using Gemini AI
- Generate AI-powered resume scores
- Identify missing skills for a target role
- Provide actionable improvement suggestions
- Store analysis history in SQLite database
- View previous resume analyses



## Tech Stack

### Backend
- Python
- Flask

### Database
- SQLite

### AI Integration
- Google Gemini API

### Frontend
- HTML
- CSS

### Other Libraries
- PyPDF
- python-dotenv

### Version Control
- Git
- GitHub



## Project Workflow

1. User uploads a PDF resume.
2. Flask receives the uploaded file.
3. Resume text is extracted using PyPDF.
4. The extracted text and target role are sent to Gemini AI.
5. Gemini evaluates the resume and generates:
   - Resume Score
   - Missing Skills
   - Improvement Suggestions
6. Results are displayed to the user.
7. Analysis history is stored in SQLite for future reference.



## Database Design

Table: analysis

| Column      | Description              |
|----------   |-------------             |
| id          | Unique analysis ID       |
| target_role | Role selected by user    |
| resume_text | Extracted resume content |
| feedback    | AI-generated analysis    |
| upload_date | Timestamp of analysis    |



## Installation

Clone the repository:

bash git clone https://github.com/nehacodes05/ai-resume-analyzer.git cd ai-resume-analyzer 

Create a virtual environment:

bash python -m venv .venv 

Activate the environment:

bash .venv\Scripts\activate 

Install dependencies:

bash pip install -r requirements.txt 

Create a .env file:

env GEMINI_API_KEY=your_api_key_here 

Run the application:

bash python app.py 

Open:

text http://127.0.0.1:5000 



## Key Concepts Demonstrated

- File Upload Handling
- PDF Processing
- API Integration
- Prompt Engineering
- Database Operations
- CRUD Concepts
- Environment Variable Management
- Git & GitHub Workflow



## Future Improvements

- User Authentication
- ATS Compatibility Scoring
- Resume Comparison Feature
- Resume Download as PDF
- PostgreSQL Integration
- FastAPI Migration
- Cloud Deployment



## Author

Neha

Built as a backend-focused portfolio project to demonstrate Flask, SQLite, PDF processing, AI integration, and database management skills.