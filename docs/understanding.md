# HireFlow AI – Project Understanding Document

## 1. Project Overview

HireFlow AI is an AI-powered recruitment platform designed to simplify the hiring process by connecting **Enterprises** and **Recruiters** through intelligent resume matching and application tracking.

The platform allows enterprises to post job openings, while recruiters upload candidate resumes, evaluate candidates using AI, and manage the hiring pipeline.

---

## 2. Problem Statement

Recruiters often receive hundreds of resumes for a single job opening. Manually screening each resume is time-consuming and inconsistent.

This project aims to automate the initial screening process by comparing resumes with job descriptions and generating ranked candidates with match scores and explanations.

---

## 3. Objectives

* Reduce manual resume screening.
* Improve candidate shortlisting using AI.
* Provide a centralized recruitment workflow.
* Track candidate progress throughout the hiring process.

---

## 4. User Roles

### Enterprise

The Enterprise represents a company that creates job opportunities.

**Responsibilities**

* Register and Login
* Create job openings
* Add required skills
* Write job descriptions
* View and manage posted jobs

### Recruiter

The Recruiter manages candidates and recruitment activities.

**Responsibilities**

* Register and Login
* Upload candidate resumes
* Manage candidate profiles
* Run AI resume matching
* Shortlist candidates
* Update application status

---

## 5. Complete Workflow

1. Enterprise logs into the platform.
2. Enterprise creates a new job posting.
3. Recruiter uploads candidate resumes.
4. Recruiter selects a job opening.
5. AI compares resumes with the Job Description.
6. The system generates match scores and explanations.
7. Recruiter shortlists suitable candidates.
8. Candidate status is updated until final selection.

---

## 6. Core Features

### Authentication

Secure role-based login for Enterprise and Recruiter users.

### Job Management

Enterprises can create, edit, and manage multiple job openings.

### Resume Management

Recruiters upload PDF resumes, and the system stores both the resume file and extracted text for AI analysis.

### AI Resume Matching

The AI evaluates candidate resumes against the selected job description and produces:

* Match Score
* Candidate Ranking
* Short Explanation

### Application Tracking

Candidates move through the recruitment pipeline:

**Applied → Shortlisted → Interviewed → Selected / Rejected**

---

## 7. Expected Deliverables

* Working web application
* AI-powered resume matching
* MySQL database
* Project documentation
* GitHub source code
* Demo presentation

---

## 8. Success Criteria

The platform will be considered successful if it can:

* Allow enterprises to post jobs.
* Allow recruiters to upload resumes.
* Generate AI-based candidate rankings.
* Track application status efficiently.
* Maintain accurate and organized recruitment records.

---

## 9. Proposed Technology Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Frontend        | HTML, CSS, JavaScript |
| Backend         | Python (Flask)        |
| Database        | MySQL                 |
| AI              | OpenAI API (LLM)      |
| Version Control | Git & GitHub          |

---

## 10. Conclusion

HireFlow AI focuses on building a practical recruitment solution that combines role-based job management with AI-assisted resume evaluation. The project emphasizes clean architecture, modular development, and real-world hiring workflows suitable for modern recruitment systems.

**Prepared by:** Poruri Nageswara Sumanth
