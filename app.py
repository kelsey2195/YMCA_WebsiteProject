from flask import Flask, render_template, redirect, request, session
import mysql.connector
import re

email_format = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

app = Flask(__name__)
app.secret_key = "27eduCBA09"

# Connection to the database
connection = mysql.connector.connect(host='localhost', password = '', user='root', database = 'flask')

@app.route('/')
def home():
    session["logging_in"] = False
    session["viewing_account"] = False
    return render_template('index.html')

@app.route('/login', methods= ['POST', 'GET'])
def log_in():
    if( 'username' in session ):
        return redirect('/')
    else:
        session["logging_in"] = True
        if request.method == 'POST':
            try:
                email = request.form['email']
                password = request.form['password']

                errorDict = {}

                cursor = connection.cursor(prepared=True)
                query = ''' SELECT * FROM employees WHERE employee_id = %s AND employee_password = %s'''
                cursor.execute(query, ( email, password ))
                result = cursor.fetchall()
                if result:
                    session["user_id"] = "employee"
                    session["username"] = result[0][1] + result[0][2]
                    session["manager_or_not"] = result[0][4]
                    cursor.close()
                    return redirect("/")

                if not re.fullmatch(email_format, email):
                    errorDict["email_error"] = "Invalid email format"

                if not email:
                    errorDict["email_error"] = "Email input must be filled"
                
                if not password:
                    errorDict["password_error"] = "Password input must be filled"
                
                if errorDict:
                    return render_template('log_in.html', 
                        email_error = errorDict.get("email_error",""),
                        password_error = errorDict.get("password_error",""), 
                        email = email)

                cursor = connection.cursor(prepared=True)
                query = ''' SELECT * FROM users WHERE email = %s AND password = %s'''
                cursor.execute(query, ( email, password ))

                message = ""
                result = cursor.fetchall()
                if result :
                    session["user_id"] = result[0][0]
                    session["username"] = result[0][1]
                    session["member_or_not"] = result[0][3]
                    cursor.close()

                    return redirect("/user_profile")
                else:
                    message = "Invalid email or password"
                    cursor.close()

                    return render_template('log_in.html', message = message, email = email)

            except mysql.connector.Error as error:
                print("Failed to login: {}".format(error))

        return render_template('log_in.html')

@app.route('/logout', methods= ['POST', 'GET'])
def log_out():
    session.clear()
    return redirect("/")

@app.route('/register_user', methods= ['POST', 'GET'])
def register_user():
    if( 'username' in session ):
        return redirect('/')
    else:
        session["logging_in"] = True

        if request.method == 'POST':
            try:
                email = request.form['email']
                username = request.form['username']
                password = request.form['password']
                verify_password = request.form['verify_password']
                membership = 0

                if request.form.get('membership'):
                    membership = 1
                    
                errorDict = {}

                if not re.fullmatch(email_format, email):
                    errorDict["email_error"] ="Invalid email format"
                
                if not password == verify_password:
                    errorDict["password_error"] = "Passwords must match"

                if( not email ):
                    errorDict["email_error"] = "Must fill email input"
                if( not username ):
                    errorDict["username_error"] = "Must fill username input"
                if( not password ):
                    errorDict["password_error"] = "Must fill password input"

                if ' ' in username:
                    errorDict["username_error"] = "Can't have white space in username"

                if ' ' in password:
                    errorDict["password_error"] = "Can't have white space in password"
                
                cursor = connection.cursor(prepared=True)
                query = ''' SELECT * FROM users WHERE email = %s'''
                cursor.execute(query, ( email, ))
                result = cursor.fetchall()

                if result :
                    cursor.close()
                    errorDict["email_error"] = "Email already in use"


                if errorDict:
                    return render_template('register.html',
                        email_error = errorDict.get("email_error",""),
                        username_error = errorDict.get("username_error",""),
                        password_error = errorDict.get("password_error",""),
                        email = email, username = username)

                cursor = connection.cursor(prepared=True)
            
                query = ''' INSERT INTO users VALUES(?,?,?,?)'''
                cursor.execute(query, ( email, username, password, membership ))
                
                connection.commit()
                
                cursor.close()
            
                session["user_id"] = email
                session["username"] = username
                session["member_or_not"] = membership

                return redirect("/user_profile")
                
            except mysql.connector.Error as error:
                print("Failed to register: {}".format(error))
        
        return render_template("register.html")

@app.route('/user_profile') 
def user_profile():
    if( 'user_id' in session ):
        if( session['user_id'] == "employee" ):
            return redirect("/")
    if( 'username' not in session ):
        return redirect('/login')  
    else:
        session["viewing_account"] = True
        cursor = connection.cursor(prepared=True)
        query = ''' SELECT *
                    FROM accounts LEFT OUTER JOIN swim_levels 
                    ON accounts.account_level = swim_levels.swim_level_id 
                    WHERE associated_user = ?'''
        cursor.execute(query, ( session["user_id"], ))

        result = cursor.fetchall()

        num = cursor.rowcount
        cursor.close()

        return render_template("user_profile.html", accounts = result, num_accounts = num)


@app.route('/create_program', methods= ['POST', 'GET'])
def create_program():
    if( session['user_id'] != "employee" and session["manager_or_not"] != 1 ):
        return redirect("/create_program.html")
    else:
        print("Place holder")






if __name__ == "__main__":
    app.run()