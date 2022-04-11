from flask import Flask, render_template, redirect, request, session
import mysql.connector
import re

email_format = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

app = Flask(__name__)
app.secret_key = "27eduCBA09"

# Connection to the database
connection = mysql.connector.connect(host='localhost', password = '', user='root', database = 'flask')

# Home
@app.route('/')
def home():
    # set session variable sback to false to show various buttons
    session["logging_in"] = False
    session["viewing_account"] = False
    return render_template('index.html')

# Login for employees and users
@app.route('/login', methods= ['POST', 'GET'])
def login():
    if( 'username' in session ):    # checks if you are already logged in
        return redirect('/')
    else:
        session["logging_in"] = True # hide login button
        if request.method == 'POST':
            try:
                # capture form elements
                email = request.form['email']
                password = request.form['password']

                errorDict = {}  # create dictonary to hold errors for printing

                # This block checks if the login is an employee
                cursor = connection.cursor(prepared=True)
                query = ''' SELECT * FROM employees WHERE employee_id = %s AND employee_password = %s'''
                cursor.execute(query, ( email, password ))
                result = cursor.fetchall()
                # Sets session to contain employee information
                if result:
                    session["user_id"] = "employee"
                    session["username"] = result[0][1] + result[0][2]
                    session["manager_or_not"] = result[0][4]
                    cursor.close()
                    return redirect("/")

                # If it's not an employee login apply rules to check if it's right format ect.
                # check if it's email in the right format
                if not re.fullmatch(email_format, email):
                    errorDict["email_error"] = "Invalid email format"

                # check if email is empty
                if not email:
                    errorDict["email_error"] = "Email input must be filled"
                
                # check if password is empty
                if not password:
                    errorDict["password_error"] = "Password input must be filled"
                
                # if there were errors 
                if errorDict:
                    return render_template('log_in.html', 
                        email_error = errorDict.get("email_error",""),
                        password_error = errorDict.get("password_error",""), 
                        email = email)

                # no errors on input -> now check if this is a valid user
                # fetches the input from the databse
                cursor = connection.cursor(prepared=True)
                query = ''' SELECT * FROM users WHERE email = %s AND password = %s'''
                cursor.execute(query, ( email, password ))

                result = cursor.fetchall()

                # if there is a result then that means it's a valid user
                if result :
                    # fill session info with user information
                    session["user_id"] = result[0][0]
                    session["username"] = result[0][1]
                    session["member_or_not"] = result[0][3]
                    cursor.close()

                    return redirect("/user_profile")
                else:
                    # invalid user
                    message = "Invalid email or password"
                    cursor.close()
                    return render_template('log_in.html', message = message, email = email)
            
            # exception handler
            except mysql.connector.Error as error:
                print("Failed to login: {}".format(error))

        return render_template('log_in.html')

# logout just clears out session information and sets you back to home page
@app.route('/logout', methods= ['POST', 'GET'])
def log_out():
    session.clear()
    return redirect("/")

# Creates a new user 
@app.route('/register_user', methods= ['POST', 'GET'])
def register_user():
    if( 'username' in session ):
        return redirect('/')    # checks to make sure user was already created
    else:
        session["logging_in"] = True

        if request.method == 'POST':
            try:
                # caputure result from form
                email = request.form['email']
                username = request.form['username']
                password = request.form['password']
                verify_password = request.form['verify_password']
                membership = 0

                # checks if the membership redial is checked
                if request.form.get('membership'):
                    membership = 1      # if it is checked then is the user wants to have a membership
                    
                # create dict to fill with errors
                errorDict = {}

                # checks if the email is valid format
                if not re.fullmatch(email_format, email):
                    errorDict["email_error"] ="Invalid email format"
                
                # checks to make sure passowrds match
                if not password == verify_password:
                    errorDict["password_error"] = "Passwords must match"

                # checks if the email input is empty
                if( not email ):
                    errorDict["email_error"] = "Must fill email input"

                # checks if the username input is empty
                if( not username ):
                    errorDict["username_error"] = "Must fill username input"

                # checks if the password input is empty
                if( not password ):
                    errorDict["password_error"] = "Must fill password input"

                # Checks if there are whites spaces in either username or password
                if ' ' in username:
                    errorDict["username_error"] = "Can't have white space in username"
                if ' ' in password:
                    errorDict["password_error"] = "Can't have white space in password"
                
                # Checks if that email is already in user
                cursor = connection.cursor(prepared=True)
                query = ''' SELECT * FROM users WHERE email = %s'''
                cursor.execute(query, ( email, ))
                result = cursor.fetchall()

                # if there is a result that means that the email is in use
                if result :
                    cursor.close()
                    errorDict["email_error"] = "Email already in use"

                # Checks if there was any errors
                if errorDict:
                    # return register template with errors on display
                    return render_template('register.html',
                        email_error = errorDict.get("email_error",""),
                        username_error = errorDict.get("username_error",""),
                        password_error = errorDict.get("password_error",""),
                        email = email, username = username)

                # now enter the information into database
                cursor = connection.cursor(prepared=True)
                query = ''' INSERT INTO users VALUES(?,?,?,?)'''
                cursor.execute(query, ( email, username, password, membership ))
                connection.commit()
                cursor.close()
            
                # set session information
                session["user_id"] = email
                session["username"] = username
                session["member_or_not"] = membership

                return redirect("/user_profile")

            # exception handler    
            except mysql.connector.Error as error:
                print("Failed to register: {}".format(error))
        
        return render_template("register.html")

# user profile
@app.route('/user_profile') 
def user_profile():
    # checks to make sure that the user isn't an employee
    if( 'user_id' in session ): # first checks if user_id is in session so you don't get a null error
        # checks if employee
        if( session['user_id'] == "employee" ):
            return redirect("/")   #<--- TODO eventually need to add a redirect to employee account page
    
    # checks if the user is logged in
    if( 'username' not in session ):
        return redirect('/login')  
    else:
        # variable in session to hide account button
        session["viewing_account"] = True

        # collect user information & all their associated accounts
        cursor = connection.cursor(prepared=True)
        query = ''' SELECT *
                    FROM accounts LEFT OUTER JOIN swim_levels 
                    ON accounts.account_level = swim_levels.swim_level_id 
                    WHERE associated_user = ?'''
        cursor.execute(query, ( session["user_id"], ))
        result = cursor.fetchall()

        # TODO eventually this will have to be formated for output in a nice looking way
        num = cursor.rowcount
        cursor.close()
        return render_template("user_profile.html", accounts = result, num_accounts = num)

# Will eventually have the ability to create a program here
# only manager's should be able to create programs
@app.route('/create_program', methods= ['POST', 'GET'])
def create_program():
    # catches regular employess and users here
    if( session['user_id'] != "employee" or session["manager_or_not"] != 1 ):
        return redirect("/")
    else:
        return render_template("create_program.html")


if __name__ == "__main__":
    app.run()