from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("login.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT * FROM users
        WHERE email=%s AND password=%s AND role=%s
    """,(email,password,role))

    user = cur.fetchone()
    cur.close()

    if user:
        if role == "enterprise":
            return redirect("/enterprise")
        else:
            return redirect("/recruiter")

    return "Invalid Email / Password / Role"


# ---------------- ENTERPRISE DASHBOARD ----------------

@app.route("/enterprise")
def enterprise():

    cur = mysql.connection.cursor()

    # Total Jobs
    cur.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cur.fetchone()[0]

    # Active Jobs
    active_jobs = total_jobs

    # Applicants (Phase 1)
    total_applicants = 0

    # Recent Jobs
    cur.execute("""
        SELECT title, department, location
        FROM jobs
        ORDER BY created_at DESC
        LIMIT 5
    """)

    recent_jobs = cur.fetchall()
    cur.close()

    return render_template(
        "enterprise_dashboard.html",
        total_jobs=total_jobs,
        active_jobs=active_jobs,
        total_applicants=total_applicants,
        recent_jobs=recent_jobs
    )


# ---------------- RECRUITER DASHBOARD ----------------

@app.route("/recruiter")
def recruiter():
    return render_template("recruiter_dashboard.html")


# ---------------- CREATE JOB PAGE ----------------

@app.route("/new-job")
def new_job():
    return render_template("create_job.html")


# ---------------- SAVE JOB ----------------

@app.route("/create-job", methods=["POST"])
def create_job():

    title = request.form["title"]
    department = request.form["department"]
    location = request.form["location"]
    job_type = request.form["job_type"]
    salary = request.form["salary"]
    skills = request.form["skills"]
    description = request.form["description"]

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO jobs
        (title, department, location, job_type, salary, skills, description, created_by)

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """,(
        title,
        department,
        location,
        job_type,
        salary,
        skills,
        description,
        1
    ))

    mysql.connection.commit()
    cur.close()

    return redirect("/jobs")


# ---------------- MY JOBS ----------------

@app.route("/jobs")
def jobs():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT title, department, location, job_type, salary
        FROM jobs
        ORDER BY created_at DESC
    """)

    jobs = cur.fetchall()
    cur.close()

    return render_template("jobs.html", jobs=jobs)


if __name__ == "__main__":
    app.run(debug=True)