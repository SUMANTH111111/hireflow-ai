# HireFlow AI – System Architecture

## Project Architecture

HireFlow AI follows a **3-tier architecture**, separating the presentation layer, business logic, and database. This modular design improves maintainability, scalability, and code organization.

### Architecture Overview

**Presentation Layer**

* HTML
* CSS
* JavaScript

↓

**Application Layer**

* Python (Flask)
* Authentication
* Job Management
* Resume Management
* AI Matching Engine

↓

**Data Layer**

* MySQL Database

---

## User Roles

### Enterprise

* Register and Login
* Create, edit, and delete job openings
* View posted jobs

### Recruiter

* Register and Login
* Upload candidate resumes
* Manage candidate profiles
* Run AI resume matching
* Update application status

---

## Core Modules

### Authentication Module

Handles secure login and role-based access for Enterprise and Recruiter users.

### Job Management Module

Allows enterprises to create job postings with role details, required skills, and job descriptions.

### Resume Management Module

Recruiters upload PDF resumes. The system stores both the file path and extracted resume text for AI analysis.

### AI Matching Module

The extracted resume text is compared with the selected Job Description. The AI generates:

* Match Score
* Ranking
* Short Explanation

### Application Tracking Module

Each candidate progresses through the hiring pipeline:

Applied → Shortlisted → Interviewed → Selected / Rejected

---

## Database Design

The system contains four normalized tables:

* **users** – Enterprise and Recruiter accounts
* **jobs** – Job openings
* **candidates** – Resume records
* **applications** – AI scores and hiring status

The `applications` table acts as a bridge between jobs and candidates, enabling a candidate to apply for multiple jobs while maintaining separate scores and statuses.

---

## Technology Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Frontend        | HTML, CSS, JavaScript |
| Backend         | Python (Flask)        |
| Database        | MySQL                 |
| AI              | OpenAI API (LLM)      |
| Version Control | Git & GitHub          |

---

## Design Decisions

* A single **users** table is used with role-based access instead of separate authentication tables.
* Resume PDFs are preserved while extracted text is stored for efficient AI analysis.
* The application follows a modular folder structure to simplify future expansion and maintenance.
* MySQL foreign keys maintain data integrity between users, jobs, candidates, and applications.
