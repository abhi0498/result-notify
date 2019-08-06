from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
import json
from flask_sqlalchemy import SQLAlchemy
from os import environ
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Mail(db.Model):
    email = db.Column(db.String(120), unique=True, primary_key=True)
    sem = db.Column(db.Integer)

    def __repr__(self):
        name = self.email.split('@')
        return '<Mail %r>' % name[0]


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':

        user = request.form['email']
        sem = request.form['semester']
        mail = Mail(email=user, sem=sem)
        db.session.add(mail)
        db.session.commit()
        name = user.split('@')
        return redirect(url_for('success', name=name[0]))

    else:
        students = list(Mail.query.all())
        student_mail = [student.email for student in students]
        return render_template("form.html", mail=student_mail)


@app.route('/success/?name=<name>')
def success(name):
    return render_template("success.html", name=name)


# @app.route("/mail", methods=["POST", "GET"])
# def mail():
#     if request.method == 'POST':

#         user = request.form['email']
#         sem = request.form['semester']
#         mail = Mail(email=user, sem=sem)
#         db.session.add(mail)
#         db.session.commit()
#         name = user.split('@')

#         return redirect(url_for('success', name=name[0]))
#     else:
#         return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
