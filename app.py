from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# ---------- MySQL ----------
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Root@991241"
app.config["MYSQL_DB"] = "hireflow_ai"

mysql = MySQL(app)

# ---------- Login ----------
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s AND role=%s",
        (email, password, role)
    )

    user = cur.fetchone()
    cur.close()

    if user:
        if role == "enterprise":
            return redirect("/enterprise")

        return redirect("/recruiter")

    return "Invalid credentials"

# ---------- Dashboards ----------
@app.route("/enterprise")
def enterprise():
    return render_template("enterprise_dashboard.html")

@app.route("/recruiter")
def recruiter():
    return render_template("recruiter_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)