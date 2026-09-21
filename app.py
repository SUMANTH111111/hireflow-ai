from flask import Flask
from config import Config
from models.db import mysql

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)

@app.route("/")
def home():
    return "HireFlow AI is Running 🚀"

if __name__ == "__main__":
    app.run(debug=True)