from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from config import Config

import pymupdf
import os

from ai.matcher import calculate_match

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

# ==========================================
# UPLOAD FOLDER
# ==========================================

UPLOAD_FOLDER = "static/uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("login.html")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT user_id, name
        FROM users
        WHERE email=%s
        AND password=%s
        AND role=%s
    """, (email, password, role))

    user = cur.fetchone()
    cur.close()

    if not user:
        return "Invalid Email / Password"

    if role == "enterprise":
        return redirect("/enterprise")

    return redirect("/recruiter")


# ==========================================
# ENTERPRISE DASHBOARD
# ==========================================

@app.route("/enterprise")
def enterprise():

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM applications")
    total_applicants = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM jobs")
    active_jobs = cur.fetchone()[0]

    cur.execute("""
        SELECT title, department, location
        FROM jobs
        ORDER BY created_at DESC
        LIMIT 5
    """)

    rows = cur.fetchall()

    recent_jobs = []

    for row in rows:
        recent_jobs.append({
            "title": row[0],
            "department": row[1],
            "location": row[2]
        })

    cur.close()

    return render_template(
        "enterprise_dashboard.html",
        total_jobs=total_jobs,
        total_applicants=total_applicants,
        active_jobs=active_jobs,
        recent_jobs=recent_jobs
    )


# ==========================================
# RECRUITER DASHBOARD
# ==========================================

@app.route("/recruiter")
def recruiter():

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM candidates")
    total_resumes = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status='Shortlisted'
    """)
    shortlisted = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE status='Interviewed'
    """)
    interviewed = cur.fetchone()[0]

    # Job Dropdown

    cur.execute("""
        SELECT job_id, title
        FROM jobs
        ORDER BY created_at DESC
    """)

    job_rows = cur.fetchall()

    jobs = []

    for row in job_rows:
        jobs.append({
            "job_id": row[0],
            "title": row[1]
        })

    # Recent Applications

    cur.execute("""
        SELECT
            c.full_name,
            j.title,
            a.match_score,
            a.status
        FROM applications a
        JOIN candidates c
            ON a.candidate_id = c.candidate_id
        JOIN jobs j
            ON a.job_id = j.job_id
        ORDER BY a.applied_at DESC
        LIMIT 5
    """)

    rows = cur.fetchall()

    applications = []

    for row in rows:
        applications.append({
            "full_name": row[0],
            "title": row[1],
            "match_score": row[2],
            "status": row[3]
        })

    cur.close()

    return render_template(
        "recruiter_dashboard.html",
        total_resumes=total_resumes,
        shortlisted=shortlisted,
        interviewed=interviewed,
        jobs=jobs,
        applications=applications
    )


# ==========================================
# CREATE JOB PAGE
# ==========================================

@app.route("/new-job")
def new_job():
    return render_template("create_job.html")


# ==========================================
# SAVE JOB
# ==========================================

@app.route("/create-job", methods=["POST"])
def create_job():

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO jobs
        (
            title,
            department,
            location,
            job_type,
            salary,
            skills,
            description,
            created_by
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (

        request.form["title"],
        request.form["department"],
        request.form["location"],
        request.form["job_type"],
        request.form["salary"],
        request.form["skills"],
        request.form["description"],
        1

    ))

    mysql.connection.commit()
    cur.close()

    return redirect("/enterprise")


# ==========================
# RECRUITER / MY JOBS
# ==========================

@app.route("/jobs")
def jobs():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            title,
            department,
            location,
            job_type,
            salary
        FROM jobs
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()

    jobs = []

    for row in rows:
        jobs.append({
            "title": row[0],
            "department": row[1],
            "location": row[2],
            "job_type": row[3],
            "salary": row[4]
        })

    cur.close()

    return render_template("jobs.html", jobs=jobs)


# ==========================
# ENTERPRISE MY JOBS
# ==========================

@app.route("/enterprise/jobs")
def enterprise_jobs():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            title,
            department,
            location,
            job_type,
            salary
        FROM jobs
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()

    jobs = []

    for row in rows:
        jobs.append({
            "title": row[0],
            "department": row[1],
            "location": row[2],
            "job_type": row[3],
            "salary": row[4]
        })

    cur.close()

    return render_template("jobs.html", jobs=jobs)

# ==========================================
# AI RESUME UPLOAD
# ==========================================

@app.route("/upload-resume", methods=["POST"])
def upload_resume():

    full_name = request.form["full_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    job_id = request.form["job_id"]

    pdf = request.files["resume"]

    filename = secure_filename(pdf.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    pdf.save(filepath)

    # -------- Extract Resume Text --------

    extracted_text = ""

    document = pymupdf.open(filepath)

    for page in document:
        extracted_text += page.get_text()

    document.close()

    # -------- Fetch Job Details --------

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT description, skills
        FROM jobs
        WHERE job_id=%s
    """, (job_id,))

    job = cur.fetchone()

    job_description = job[0]
    job_skills = job[1]

    # -------- AI Matching --------

    score, explanation = calculate_match(
        extracted_text,
        job_description,
        job_skills
    )

    # -------- Save Candidate --------

    cur.execute("""
        INSERT INTO candidates
        (
            full_name,
            email,
            phone,
            resume_file,
            extracted_text
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (

        full_name,
        email,
        phone,
        filename,
        extracted_text

    ))

    candidate_id = cur.lastrowid

    # -------- Decision Logic --------

    if score >= 85:
        status = "Shortlisted"
    elif score >= 60:
        status = "Applied"
    else:
        status = "Rejected"

    # -------- Save Application --------

    cur.execute("""
        INSERT INTO applications
        (
            job_id,
            candidate_id,
            match_score,
            explanation,
            status
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (

        job_id,
        candidate_id,
        score,
        explanation,
        status

    ))

    mysql.connection.commit()
    cur.close()

    return redirect("/recruiter")


# ==========================================
# RECRUITER APPLICATIONS
# ==========================================

@app.route("/applications")
def applications():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            c.full_name,
            c.email,
            j.title,
            a.match_score,
            a.explanation,
            a.status
        FROM applications a
        JOIN candidates c
            ON a.candidate_id = c.candidate_id
        JOIN jobs j
            ON a.job_id = j.job_id
        ORDER BY a.applied_at DESC
    """)

    rows = cur.fetchall()

    apps = []

    for row in rows:
        apps.append({
            "name": row[0],
            "email": row[1],
            "job": row[2],
            "score": row[3],
            "explanation": row[4],
            "status": row[5]
        })

    cur.close()

    return render_template(
        "applications.html",
        apps=apps
    )
# ==========================================
# ANALYTICS
# ==========================================

@app.route("/analytics")
def analytics():

    cur = mysql.connection.cursor()

    # Jobs by Department
    cur.execute("""
        SELECT department, COUNT(*)
        FROM jobs
        GROUP BY department
        ORDER BY COUNT(*) DESC
    """)

    dept_rows = cur.fetchall()

    departments = []
    department_counts = []

    for row in dept_rows:
        departments.append(row[0])
        department_counts.append(row[1])

    # Applications by Status
    cur.execute("""
        SELECT status, COUNT(*)
        FROM applications
        GROUP BY status
    """)

    status_rows = cur.fetchall()

    statuses = []
    status_counts = []

    for row in status_rows:
        statuses.append(row[0])
        status_counts.append(row[1])

    cur.close()

    return render_template(
        "analytics.html",
        departments=departments,
        department_counts=department_counts,
        statuses=statuses,
        status_counts=status_counts
    )

# ==========================================
# ENTERPRISE APPLICATIONS
# ==========================================

@app.route("/enterprise/applications")
def enterprise_applications():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            a.application_id,
            c.full_name,
            c.email,
            c.resume_file,
            j.title,
            a.match_score,
            a.explanation,
            a.status
        FROM applications a
        JOIN candidates c
            ON a.candidate_id = c.candidate_id
        JOIN jobs j
            ON a.job_id = j.job_id
        ORDER BY a.applied_at DESC
    """)

    rows = cur.fetchall()
    cur.close()

    applicants = []

    for row in rows:
        applicants.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "resume": row[3],
            "job": row[4],
            "score": row[5],
            "explanation": row[6],
            "status": row[7]
        })

    return render_template(
        "enterprise_applications.html",
        applicants=applicants
    )


# ==========================================
# UPDATE APPLICATION STATUS
# ==========================================

@app.route("/update-status/<int:id>", methods=["POST"])
def update_status(id):

    new_status = request.form["status"]

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE applications
        SET status=%s
        WHERE application_id=%s
    """, (new_status, id))

    mysql.connection.commit()
    cur.close()

    return redirect("/enterprise/applications")


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():
    return redirect("/")


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)