from flask import render_template, redirect, session, url_for, request, json, g
from facebook import get_user_from_cookie, GraphAPI
from app import app
from app import api
from app import models
from app import db
import encodings

@app.template_global()
def is_empty(item):
    if isinstance(item, type(None)):
        return True
    elif item == "":
        return True
    return False


@app.route("/main")
@app.route('/index')
@app.route('/')
def home():
    return render_template('home.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    error = None
    if request.method == "POST":
        users = models.User.query.filter_by(username=request.form["username"].lower()).all()
        if len(users) > 0:
            return "ERROR: El Nombre de Usuario ya esta Registrado"
        else:
            user = models.User(request.form["username"], request.form["email"], request.form["password"])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/users")
def users():
    users_list = models.User.query.all()
    return render_template("users.html", users=users_list)


@app.route("/courses")
def courses():
    return render_template("courses.html", courses=models.Topic.query.all())

@app.route("/courses/<course>/q/<int:num>")
def questions(course, num):
    topic = models.Topic.query.filter_by(name=course.encode('utf-8')).first()
    question = models.QuestionModel.query.filter_by(cod=num, topic=topic).first()
    return render_template("question.html", question=question)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

