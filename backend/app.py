from flask import Flask, render_template

from config import Config
from extensions import db, bcrypt

from routes.auth import auth
from routes.resume import resume
from flask import Flask, render_template, send_from_directory
from flask import session, redirect, url_for



app = Flask(__name__)

# Configuration
app.config.from_object(Config)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Initialize Extensions
db.init_app(app)
bcrypt.init_app(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(resume)


# -----------------------
# Home Page
# -----------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------
# Register Page
# -----------------------
@app.route("/register_page")
def register_page():
    return render_template("register.html")


# -----------------------
# Login Page
# -----------------------
@app.route("/login_page")
def login_page():
    return render_template("login.html")


# -----------------------
# Upload Resume Page
# -----------------------
@app.route("/upload_page")
def upload_page():
    return render_template("upload.html")



@app.route("/dashboard")
@app.route("/dashboard_page")
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login_page"))



# -----------------------
# Run Application
# -----------------------
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)