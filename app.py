from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='static')

# Connection to the database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)
# Connection to the database

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
    return "hello world"

@app.route('/log_in')
def log_in():
    return render_template('log_in.html')

@app.route('/validate_login', methods= ['POST', 'GET'])
def validate_login():
    if request.method == 'GET':
        return "Login via login form"
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO members VALUES(%s,%s,%s,%s)''',(email, "placeName", "placeSurName", password))
        mysql.connection.commit()
        cursor.close()
        return f"DONE AND IN!!!"
        #return render_template('show_all.html')

with app.test_request_context():
    print(url_for('main'))

if __name__ == '__main__':
    app.run()
