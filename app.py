from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps

from wtforms import Form, StringField, PasswordField, validators

class loginWTF(Form):
    uid = StringField("E-mail or username", validators=[validators.InputRequired(), validators.Length(min=5, max=15)])
    pwd = PasswordField("Password", validators=[validators.InputRequired(), validators.equal_to('pwd2', message="password required")])
    pwd2 = PasswordField("confirm password", validators=[validators.InputRequired()])

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

def authenticate(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if "loggedin" in session and session["loggedin"]:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))
    return decorated_func

@app.route("/")
def index():
    return render_template("index.html.j2")

@app.route("/login", methods=["GET", "POST"])
def login():
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


@app.route("/loginWTFformWithMacro", methods=["GET", "POST"])
def loginwtf():
    formWTF = loginWTF(request.form)
    if request.method == "POST":
        uid = formWTF.uid.data
        pwd = formWTF.pwd.data

        if uid == "arno@arno.com" and pwd == "0000":
            # user is logged in
            session["loggedin"] = True
            session["uid"] = uid

            return redirect(url_for("secure"))

    return render_template("login/loginWTFform.html.j2", form=formWTF)

@app.route("/logout")
@authenticate
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/secure")
@authenticate
def secure():
    return render_template("secure.html.j2")

if __name__ == '__main__':
    app.run(debug=True)