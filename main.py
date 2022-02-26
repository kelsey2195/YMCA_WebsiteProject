from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///YMCA.db'
db = SQLAlchemy(app)

class Member(db.Model):
    FirstName = db.Column(db.String(50), unique=False, nullable=False)
    LastName = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    MemberId = db.Column('member_id', db.Integer, primary_key=True)
    password = db.Column(db.String(50), unique=False, nullable=False)
    level = db.Column(db.String(50), unique=False, nullable=True)

def __init__(self, FirstName, LastName, email, password):
    self.FirstName = FirstName
    self.LastName = LastName
    self.email = email
    self.password = password

#class Employee(db.Model):
#    FirstName = db.Column(db.String(50), unique=False, nullable=False)
#    LastName = db.Column(db.String(50), unique=False, nullable=False)
#    email = db.Column(db.String(50), unique=True, nullable=False)
#    EmployeeId = db.Column('employee_id', db.Integer, primary_key=True)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/program_search')
def program_search():
    return render_template('program_search.html')

@app.route('/show_all')
def show_all():
    return render_template('show_all.html', Member = Member.query.all())

@app.route('/log_in')
def log_in():
    return render_template('log_in.html')

with app.test_request_context():
    print(url_for('main'))

if __name__ == '__main__':
    db.create_all()
    app.run()
