from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

def authenticate(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        

@app.route("/")
def index():
    return render_template("index.html.j2")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "loggedin" in session and session["loggedin"]:
        return redirect(url_for("secure"))

    if request.method == "POST":
        uid = request.form.get("uid", "")
        pwd = request.form.get("pwd", "")

        print(uid)
        print(pwd)

        if uid == "arno@arno.com" and pwd == "0000":
            # user is logged in
            session["loggedin"] = True
            session["uid"] = uid

            return redirect(url_for("secure"))

    return render_template("login/login.html")

@app.route("/secure")
@authenticate
def secure():
    return render_template("secure.html.j2")

if __name__ == '__main__':
    app.run(debug=True)