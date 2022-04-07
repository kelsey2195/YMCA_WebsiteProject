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
    return render_template('main_logged.html')

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

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/swimming')
def swimming():
    return render_template('/swimming.html')

@app.route('/create_program')
def create_program():
    return render_template('create_program.html')

@app.route('/validate_program')
def validate_program():
    # program_id = request.form['program_id']
    # program_title = request.form['program_title']
    # program_date = request.form['program_date']
    # ymca_location = request.form['ymca_location']
    # program_location = request.form['program_location']
    # max_num_participants = request.form['max_num_participants']
    # non_member_price = request.form['non_member_price']
    # member_price = request.form['member_price']
    # description = request.form['description']

    # cursor = mysql.connection.cursor()
    # cursor.execute(''' INSERT INTO program_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(program_id, program_title, program_date, ymca_location, program_location, 
    #                                                                                         max_num_participants, non_member_price, member_price, description))
    # mysql.connection.commit()
    # cursor.close()
    return success()

@app.route('/validate_login', methods= ['POST', 'GET'])
def validate_login():
    # if request.method == 'GET':
# 
    # if request.method == 'POST':
    #     email = request.form['email']
    #     password = request.form['password']

    #     cursor = mysql.connection.cursor()
    #     cursor.execute(''' INSERT INTO members VALUES(%s,%s,%s,%s)''',(email, "placeName", "placeSurName", password))
    #     mysql.connection.commit()
    #     cursor.close()
    #     return main()
    return success()

with app.test_request_context():
    print(url_for('main'))

if __name__ == '__main__':
    app.run()
