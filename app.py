# app.py
import os
from flask import Flask, render_template, request, url_for, redirect


basedir = os.path.abspath(os.path.dirname(__file__)) # This is to set the working directory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database2.db') # Define the database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Options

#db = SQLAlchemy(app) # Initiate a db instance

from my_models import *
db.init_app(app)

@app.route('/')
def index():
    if not os.path.exists(os.path.join(basedir, 'database2.db')):
        db.create_all()
    return render_template('index.html')


@app.route('/show')
def show_data():
    #students = Student.query.all()
    return render_template('show.html')

@app.route('/dash_std')
def dash_students():
    students = Student.query.all()
    return render_template('dashboard_students.html', xyz=students)

@app.route('/dash_pst')
def dash_posts():
    posts = Post.query.all()
    return render_template('dashboard_posts.html', abc = posts)


@app.route('/create', methods=('GET', 'POST'))
def create_student():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          age=age,
                          bio=bio)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('dash_students'))
    return render_template('create_student.html')

@app.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('show_data'))

    return render_template('edit.html', student=student)


# No need to use a route, directly a post decorator
#@app.post('/<int:student_id>/delete/') # Starting from Flask 2.0
@app.route('/<int:student_id>/delete/', methods=['POST'])

def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('show_data'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5005)