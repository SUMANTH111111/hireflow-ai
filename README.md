# HireFlow AI — Intelligent Recruitment & Applicant Tracking System

> AI-powered recruitment platform built with **Flask, MySQL, Google Gemini, and PyMuPDF**.

## Overview

HireFlow AI is a full-stack Recruitment & Applicant Tracking System (ATS) developed as an AI Internship Assessment project. The platform provides two separate user roles:

* **Enterprise** — Creates and manages job openings.
* **Recruiter** — Uploads candidate resumes, runs AI-powered resume matching, and manages the hiring pipeline.

The application uses **Google Gemini 3.6 Flash** to analyze resumes against job descriptions and generate a match score with an explanation.

---

## Features

### Enterprise Portal

* Secure Enterprise login
* Create new job openings
* Add department, salary, skills, and job description
* View all posted jobs
* View applicants for every job
* Open uploaded PDF resumes
* Update candidate hiring status

### Recruiter Portal

* Secure Recruiter login
* Upload candidate PDF resumes
* Automatically extract resume text
* AI-powered resume screening
* Match score generation
* AI explanation for every candidate
* View application status

### AI Resume Matching

* Google Gemini 3.6 Flash
* Resume vs Job Description comparison
* Technical skill matching
* Experience estimation
* Missing skill identification
* Human-readable hiring explanation

### Hiring Pipeline

* Applied
* Shortlisted
* Interviewed
* Selected
* Rejected

### Analytics

* Jobs by department
* Applications by status
* Live recruitment dashboard

---

## Tech Stack

| Layer           | Technology              |
| --------------- | ----------------------- |
| Frontend        | HTML5, CSS3             |
| Backend         | Flask (Python)          |
| Database        | MySQL                   |
| AI Model        | Google Gemini 3.6 Flash |
| Resume Parsing  | PyMuPDF                 |
| Charts          | Chart.js                |
| Version Control | Git & GitHub            |

---

## Project Structure

```text
hireflow-ai/
│
├── ai/
│   ├── matcher.py
│   ├── parser.py
│   └── scorer.py
│
├── models/
│   └── db.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── login.html
│   ├── recruiter_dashboard.html
│   ├── enterprise_dashboard.html
│   ├── jobs.html
│   ├── applications.html
│   ├── enterprise_applications.html
│   ├── analytics.html
│   └── create_job.html
│
├── docs/
│   ├── architecture.md
│   └── understanding.md
│
├── app.py
├── config.py
├── database.sql
├── requirements.txt
└── README.md
```

---

## Database Design

### Main Tables

| Table        | Purpose                         |
| ------------ | ------------------------------- |
| users        | Enterprise & Recruiter accounts |
| jobs         | Job openings                    |
| candidates   | Candidate information & resumes |
| applications | AI scores and hiring status     |

### Relationship

```text
Enterprise
    │
    ▼
  Jobs
    │
    ▼
Applications
    ▲
    │
Candidates
```

---

## System Workflow

1. Enterprise logs in.
2. Enterprise creates a job with skills and job description.
3. Recruiter uploads a candidate's PDF resume.
4. Resume text is extracted using PyMuPDF.
5. Google Gemini compares the resume with the JD.
6. AI generates:

   * Match Score
   * Experience
   * Matched Skills
   * Missing Skills
   * Hiring Explanation
7. Candidate is added to the application list.
8. Enterprise reviews the resume and updates the hiring status.

---

## AI Architecture

```text
PDF Resume
      │
      ▼
PyMuPDF
(Text Extraction)
      │
      ▼
Google Gemini 3.6 Flash
      │
      ▼
AI Evaluation
      │
      ├── Match Score
      ├── Experience
      ├── Matched Skills
      ├── Missing Skills
      └── Explanation
      │
      ▼
MySQL Database
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SUMANTH111111/hireflow-ai.git
cd hireflow-ai
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 5. Configure MySQL

Update `config.py` with your database credentials.

```python
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"
MYSQL_DB = "hireflow"
```

### 6. Import Database

Import `database.sql` into MySQL.

### 7. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Demo Credentials

Use the credentials provided by the project developer, or create Enterprise and Recruiter accounts directly in the `users` table of the MySQL database.

---

## Key Design Decisions

### Why Flask?

* Lightweight
* Easy REST routing
* Simple template rendering
* Rapid development

### Why MySQL?

* Relational hiring workflow
* Strong entity relationships
* Reliable CRUD operations

### Why Google Gemini?

Instead of keyword matching, Gemini performs **semantic comparison** between resumes and job descriptions, producing more meaningful hiring recommendations.

---

## Challenges & AI Learning Log

This project intentionally used AI coding assistants during development. Important corrections made during implementation include:

| Issue                                            | Resolution                                                                                         |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Duplicate Flask routes caused endpoint conflicts | Refactored into unique Enterprise and Recruiter routes                                             |
| Enterprise Applicants redirected incorrectly     | Created dedicated enterprise routing                                                               |
| Resume parser detected incorrect experience      | Replaced local parser with Gemini semantic evaluation                                              |
| API key accidentally exposed                     | Revoked the leaked key, generated a new one, and secured the project using `.env` and `.gitignore` |

These corrections demonstrate understanding of both the implementation and the debugging process rather than relying solely on AI-generated code.

---

## Future Improvements

* Mobile Recruiter application
* Email interview notifications
* Resume ranking across multiple candidates
* JWT authentication
* Cloud deployment
* AI interview scheduling assistant

---

## Developer

**Poruri Nageswara Sumanth**

B.Tech Computer Science Engineering

AI Internship Assessment Project
