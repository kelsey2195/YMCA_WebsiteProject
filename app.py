#from pydoc import render_doc
from flask import Flask, render_template, redirect, request, session
import mysql.connector
import re, os, json

email_format = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

app = Flask(__name__)
app.secret_key = "27eduCBA09"

# Connection to the database
connection = mysql.connector.connect(host='localhost', password = '', user='root', database = 'flask')

# Home
@app.route('/')
def home():
    # set session variable sback to false to show various buttons
    return render_template('index.html')

@app.route('/staff_profile')
def staff_profile():
    if( session["user_id"] != 'employee' ):
        return redirect('/')
    return render_template("staff_profile.html")

# Login for employees and users
@app.route('/login', methods= ['POST', 'GET'])
def login():
    if( 'username' in session ):    # checks if you are already logged in
        return redirect('/')
    else:
        #session["logging_in"] = True # hide login button
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
                cursor.close()
                # Sets session to contain employee information
                print("Test1")
                if result:
                    session["user_id"] = "employee"

                    if(type(result[0][1]) == bytearray):
                        session["username"] = result[0][1].decode() + result[0][2].decode()
                    else:
                        session["username"] = result[0][1] + result[0][2]
                        
                    
                    session["manager_or_not"] = result[0][4]
                    return redirect('/staff_profile')
                print("Test2")

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
                cursor.close()

                # if there is a result then that means it's a valid user
                if result :
                    # fill session info with user information
                    if(type(result[0][0]) == bytearray):
                        session["user_id"] = result[0][0].decode()
                        session["username"] = result[0][1].decode()
                    else:
                        session["user_id"] = result[0][0]
                        session["username"] = result[0][1]
                        
        
                    session["member_or_not"] = result[0][3]
                    #cursor.close()
                

                    # collect user information & all their associated accounts
                    cursor = connection.cursor(prepared=True)
                    query = ''' SELECT *
                                    FROM accounts 
                                    WHERE associated_user = '{}'; '''.format(session["user_id"])
                    print(session["user_id"])
                    cursor.execute(query)
                    result = cursor.fetchall()
<<<<<<< HEAD
                    cursor.close()
                    print(result)

=======
                    cursor.close()  
               
>>>>>>> fba3a9cb9347584b606325771ddac6b7901dda78
                    if result:
                        accId, email, first, last, birth = zip(*result)
                        result = list(zip( accId, first, last ))
                        print(result)

                        # TODO eventually this will have to be formated for output in a nice looking way
                        session['accounts'] = result
                        print(result)
<<<<<<< HEAD
                        updateProgList()

=======
                        #updateProgList()
>>>>>>> fba3a9cb9347584b606325771ddac6b7901dda78

            
                    # finish user profile before redirecting to it
                    # return redirect("/user_profile")
                    return redirect('/')
                else:
                    # invalid user
                    message = "Invalid email or password"
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
        membership = ""
        if request.method == 'POST':
            try:
                # caputure result from form
                email = request.form['email']
                username = request.form['username']
                password = request.form['password']
                verify_password = request.form['verify_password']

                # checks if the membership redial is checked
                if request.form.get('membership'):
                    membership = "checked"      # if it is checked then is the user wants to have a membership
                    
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
                        email = email, username = username, membership = membership)

                if membership:
                    membership = 1
                else:
                    membership = 0

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

                return redirect("/create_account")

            # exception handler    
            except mysql.connector.Error as error:
                print("Failed to register: {}".format(error))
        
        return render_template("register.html", membership = membership)

# user profile
@app.route('/user_profile') 
def user_profile():
    # checks to make sure that the user isn't an employee
    if( 'user_id' in session ): # first checks if user_id is in session so you don't get a null error
        # checks if employee
        if( session['user_id'] == "employee" ):
            return redirect("/staff_profile")

    # checks if the user is logged in
    if( 'username' not in session ):
        return redirect('/login')  
    else:
        
        return render_template("user_profile.html", accounts = session['accounts'], num_accounts = len( session['accounts'] ) )

# Will eventually have the ability to create a program here
# only manager's should be able to create programs
@app.route('/create_program', methods= ['POST', 'GET'])
def create_program():
    # catches regular employess and users here
    if( session['user_id'] != "employee" or session["manager_or_not"] != 1 ):
        return redirect("/")
    else:
        dayAndTime = [ (["","","","","","",""],"","",True) ]
        numDayAndTime = 1

        if request.method == 'POST':
            try:
                # capture form information
                progname = request.form.get("program")
                startDate = request.form.get("start")
                endDate = request.form.get("end")

                # Start process time and day list
                numDayAndTime = int( request.form.get("numDayAndTime") )
                if request.form.get('add'):
                    numDayAndTime += 1

                remove = 0   
                for x in range(1, numDayAndTime + 1):
                    if request.form.get('remove' + str(x) ):
                        remove = x
                        break
                
                dayAndTime = [ createDayAndTime( x, request ) for x in range(1, numDayAndTime + 1) if x != remove ]
                numDayAndTime = len( dayAndTime )
                if( numDayAndTime <= 0 ):
                    dayAndTime = [ (["","","","","","",""],"","",True) ]
                    numDayAndTime = 1
                # end process time and day list

                # continue capturing form
                location = request.form.get("location")
                description = request.form.get("description")
                maxParticipants = request.form.get("maxParticipants")
                memberPrice = request.form.get("memberPrice")
                nonMemberPrice = request.form.get("nonMemberPrice")
                minswimlevel = request.form.get("minswimlevel")

                # not create no need to validate errors
                # captures the remove and add post
                if not request.form.get('create'):
                    return render_template("create_program.html", 
                        progname = progname,
                        startDate=startDate, endDate=endDate,
                        dayAndTime=dayAndTime, numDayAndTime=numDayAndTime,
                        location=location, description=description, maxParticipants=maxParticipants,
                        memberPrice=memberPrice, nonMemberPrice=nonMemberPrice, minswimlevel=minswimlevel )

                # create dict to fill with errors
                errorDict = {}

                # check for errors in every input
                if( not progname ):
                    errorDict["name_error"] = "Must fill name input"
                if( not startDate or not endDate ):
                    errorDict["date_error"] = "Must have a start and date"
                
                i = next( (i for i, v in enumerate(dayAndTime) if v[3] == True), -1)
                if( i > -1):
                    errorDict["daytime_error"] = "Make sure time " + str(i + 1) + " is completely filled or remove it"

                if( not location ):
                    errorDict["location_error"] = "Must have a location"

                if( not maxParticipants ):
                    errorDict["max_error"] = "Must specify the maximum participants"

                if( not memberPrice or not nonMemberPrice):
                    errorDict["price_error"] = "Must have a price for members and nonmembers"

                if( not minswimlevel ):
                    errorDict["level_error"] = "Must have a minimum level for participants of this program" 
                # elif( minswimlevel.lower() not in swimlevels ):
                #     errorDict["level_error"] = "Invalid swimlevel" 
                
                # errors so return template rendered with errors
                if errorDict:
                    return render_template("create_program.html", 
                        name_error = errorDict.get("name_error",""),
                        date_error = errorDict.get("date_error",""),
                        daytime_error = errorDict.get("daytime_error",""),
                        location_error = errorDict.get("location_error",""),
                        max_error = errorDict.get("max_error",""),
                        price_error = errorDict.get("price_error",""),
                        level_error = errorDict.get("level_error",""),
                        progname = progname,
                        startDate=startDate, endDate=endDate,
                        dayAndTime=dayAndTime, numDayAndTime=numDayAndTime,
                        location=location, description=description, maxParticipants=maxParticipants,
                        memberPrice=memberPrice, nonMemberPrice=nonMemberPrice, minswimlevel=minswimlevel, )
                else:
                     # have to acutally insert into database here
                    cursor = connection.cursor(prepared=True)
                    query = ''' INSERT INTO programs 
                                    ( `name_program`, `start_date`, `end_date`, `location`, `description`, 
                                        `min_swim_level`, `member_price`, `nonmember_price`, `num_total_people`, `num_signed_up`, `active`)
                                    VALUES (?,?,?,?,?,?,?,?,?,0,1); '''
                    cursor.execute(query, ( progname, startDate, endDate, location, description, 
                                        minswimlevel, memberPrice, nonMemberPrice, maxParticipants))
        
                    programId = cursor.lastrowid

                    dayTimeTupleList = [ dayTimeInsertTuple(x, programId) for x in dayAndTime ]
                    dayTimeTupleList =  [item for sublist in dayTimeTupleList for item in sublist] #flatten list
                    print(dayTimeTupleList)
                    query = ''' INSERT INTO program_schedule 
                                    (`program_id`, `day_of_week`, `start_time`, `end_time`) VALUES (?,?,?,?); '''

                    cursor.executemany( query, dayTimeTupleList )

                    connection.commit()
                    cursor.close()

                    print("Success")

                    return redirect("/")

            except mysql.connector.Error as error:
                print("Failed to create new program: {}".format(error))

        # Renders inital template
        return render_template("create_program.html", 
            dayAndTime=dayAndTime, numDayAndTime=numDayAndTime )

# Create account associated with user
# used initially when creating a new user and when creating a new family account
@app.route('/create_account', methods= ['POST', 'GET'])
def create_user_account():
    # catches regular employess and users here
    if(  'user_id' not in session or session['user_id'] == "employee" ):
        return redirect("/")
    elif( session["member_or_not"] == 0 and 'accounts' in session ):
        return redirect("/user_profile")
    else:
        child = "checked"
        if request.method == 'POST':
            try:
                first = request.form['first']
                last = request.form['last']

                birthday = request.form['birthday']

                # checks if the child redial is checked
                if not request.form.get('child'):
                    child = ""      # if it is not checked then new account is user

                # create dict to fill with errors
                errorDict = {}

                # Checks if there are whites spaces in either username or password
                if ' ' in first:
                    errorDict["first_error"] = "Can't have white space in name"
                if ' ' in last:
                    errorDict["last_error"] = "Can't have white space in surname"

                if( not first ):
                    errorDict["first_error"] = "Must fill name input"
                if( not last ):
                    errorDict["last_error"] = "Must fill surname input"
                if( not birthday ):
                    errorDict["birthday_error"] = "Must fill birthday input"
                else:
                    print(birthday)
                    # TODO check to make sure it's a valid date. can't be born after today can't be born more than 200 years ago today

                if errorDict:
                    # return register template with errors on display
                    return render_template('create_account.html',
                        first_error = errorDict.get("first_error",""),
                        last_error = errorDict.get("last_error",""),
                        birthday_error = errorDict.get("birthday_error",""),
                        first = first, last = last, birthday = birthday, child = child )

                # checks if the child attribute was checked or not
                if child:
                    child = 1
                else:
                    child = 0

                print("TEST1")

                # now enter the information into database
                cursor = connection.cursor(prepared=True)
                query = ''' INSERT INTO accounts (`associated_user`, `account_first_name`, `account_last_name`, `account_birth_day`) 
                            VALUES(?,?,?,?)'''
                cursor.execute(query, ( session["user_id"], first, last, birthday))
                connection.commit()
                cursor.close()

                # collect user information & all their associated accounts
                cursor = connection.cursor(prepared=True)
                query = ''' SELECT *
                            FROM accounts 
                            WHERE associated_user = ?'''
                cursor.execute(query, ( session["user_id"], ))
                result = cursor.fetchall()
                accId, email, first, last, birth = zip(*result)
                result = list(zip( accId, first, last ))
                # TODO eventually this will have to be formated for output in a nice looking way
                session['accounts'] = result
                print(result)
                cursor.close()


                # exception handler    
                return redirect("/user_profile")

            except mysql.connector.Error as error:
                print("Failed to create new account: {}".format(error))

        return render_template("create_account.html", child = child)

@app.route('/user_search')
def user_search():
    if session["user_id"] == "employee" :
        result = "empty"
        cursor = connection.cursor(prepared=True)
        query = ''' SELECT accounts.account_id, account_first_name, account_last_name, name_program, start_date, end_date, description 
                    FROM (( account_in_program 
                        INNER JOIN accounts  ON account_in_program.account_id = accounts.account_id )
                        INNER JOIN programs ON account_in_program.program_id = programs.program_id )'''
        cursor.execute( query )
        result = cursor.fetchall()
        cursor.close()
        print( result )
        create_user_table(result)

        return render_template("user_search.html")


@app.route('/program_search')
def program_search():

    if 'user_id' not in session :
        price_type = "nonmember_price"
    else:
        # Obtains the correct price for the user depending on if they are a member or not
        if not session["user_id"] != "employee" or session["member_or_not"] == 0:
                price_type = "nonmember_price"
        else:
                price_type = "member_price"

    # Queries the db for all programs
    # TODO: Implement advanced queries
    cursor = connection.cursor(prepared=True)
    query = ''' SELECT name_program, start_date, end_date, description, {}, num_total_people, num_signed_up, program_id 
                    FROM programs
                    WHERE active = 1; '''.format(price_type)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    create_table(result)

    return render_template("program_search.html")
    

@app.route('/cancel_program', methods=['POST'])
def cancel_program():
    output = request.get_json()
    result = json.loads(output)
    program_id = int(result)
    cursor = connection.cursor(prepared=True)
    query = ''' UPDATE programs SET active = 0 WHERE program_id = {}; '''.format(program_id)
    cursor.execute(query)
    connection.commit()
    cursor.close()
    return redirect('/program_search')


@app.route('/register_program', methods=['POST'])
def register_program():
    print('hello')
    # staff cannot register for programs
    if session["user_id"] == "employee":
        redirect('/program_search')

    output = request.get_json()
    program_id = int(json.loads(output))
    user_id = session["user_id"]
    cursor = connection.cursor(prepared=True)
    query = ''' INSERT INTO account_in_program VALUES (?,?); '''
    try:
        cursor.execute(query, (user_id, program_id))
        connection.commit()
        print("----------REGISTERING USER FOR PROGRAM------------")
        print("Query: " + query)
        cursor.close()
        # return redirect('/user_profile')
        return redirect('/')

    except mysql.connector.Error as error:
        # Program doesn't exist
        print("Failed to register: {}".format(error))
    cursor.close()
    return redirect('/program_search')


@app.route('/activate_all', methods=['POST'])
def activate_all():
    cursor = connection.cursor(prepared=True)
    query = ''' UPDATE programs SET active = 1; '''
    cursor.execute(query)
    connection.commit()
    cursor.close()
    return redirect('/program_search')


#Creates html file of table of available programs
#File placed in data folder as table.html
def create_table(result):
    file_path = 'templates/data/table.html'
    # Ensure that table.html has the correct data
    if os.path.exists(file_path):
        os.remove(file_path)

    # creates table.html
    file = open(file_path, "w")
    table = ""

    #Placing data from result into table.html
    for i in range(len(result)):
        table += '''  <tr  id="{}">\n'''.format(result[i][7])
        for column in range(len(result[i])-3):
            try:
                table += '''    <td>{}</td>\n'''.format(result[i][column].decode())
            except(AttributeError):
                table += "    <td>{}</td>\n".format(result[i][column])
        table += "    <td>{0}/{1}</td>\n".format(result[i][5]-result[i][6], result[i][5])
        table += " </tr>\n"

    file.writelines(table)
    file.close()

def create_user_table(result):
    file_path = 'templates/data/usertable.html'
    # Ensure that table.html has the correct data
    if os.path.exists(file_path):
        os.remove(file_path)

    # creates table.html
    file = open(file_path, "w")
    table = ""
    print(result)
    #Placing data from result into table.html
    for i in range(len(result)):
        table += "  <tr>\n"
        for column in range(5):
            try:
                table += "    <td>{0}</td>\n".format(result[i][column].decode())
            except(AttributeError):
                table += "    <td>{0}</td>\n".format(result[i][column])
        table += "    <td>{0}/{1}</td>\n".format(result[i][5]-result[i][6], result[i][5])
        table += " </tr>\n"

    file.writelines(table)
    file.close()

def createDayAndTime( x, request ):
    dayList = []
    empty = True

    if( request.form.get('sunday' + str(x)) ):
        dayList.append("checked")
        empty = False
    else:
        dayList.append("")
    if( request.form.get('monday' + str(x)) ):
        dayList.append("checked")
        empty = False
    else:
        dayList.append("")
    if( request.form.get('tuesday' + str(x)) ):
        dayList.append("checked")
        empty = False
    else:
        dayList.append("")
    if( request.form.get('wednesday' + str(x)) ):
        dayList.append("checked")
        empty = False
    else:
        dayList.append("")
    if( request.form.get('thursday' + str(x)) ):
        dayList.append("checked")
        empty = False
    else:
        dayList.append("")
    if( request.form.get('friday' + str(x)) ):
        dayList.append("checked")
        empty = False
    else:
        dayList.append("")
    if( request.form.get('saturday' + str(x)) ):
        dayList.append("checked")
        empty = False
    else:
        dayList.append("")
    
    startTime = ""
    if( request.form.get('startTime' + str(x)) ):
        startTime = request.form.get('startTime' + str(x))

    endTime = ""
    if( request.form.get('endTime' + str(x)) ):
        endTime = request.form.get('endTime' + str(x))

    if( startTime == "" or endTime == "" ):
        empty = True

    return ( dayList, startTime, endTime, empty )

def updateProgList():
     # collect user information & all their associated accounts
    cursor = connection.cursor(prepared=True)
    new = []
    for account in session['accounts']:
        query = ''' SELECT programs.program_id, name_program, start_date, end_date, day_of_week, start_time, end_time
                FROM account_in_program
                INNER JOIN accounts USING (account_id)
                INNER JOIN programs USING (program_id)
                INNER JOIN program_schedule USING (program_id)
                WHERE accounts.account_id = ?; '''
        cursor.execute(query, ( account[0], ))
        result = cursor.fetchall()
        temp = []
        for row in result:
            temp.append(row)
            #print(row)

        #print(temp)
        new.append( (account[0], temp) )

    #print()
    #print(new)
    session["programs"] = new
    cursor.close()

# takes in an input program and checks if that information already exists
#def checkConflict(accountId, programId, startDate, endDate, ):



def dayTimeInsertTuple( x, programId ):
    return [ (programId, i, x[1], x[2]) for i,day in enumerate(x[0]) if day == 'checked' ]


if __name__ == "__main__":
    app.run(debug=True)