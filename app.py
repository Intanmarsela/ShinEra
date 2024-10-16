import sqlite3
import plotly.graph_objects as go
from flask import Flask, make_response, redirect, render_template, request, session, url_for, jsonify, json
from helpers import random_string, search, templates, login_required, get_question, get_data
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime

data = {'key': 'value'}
headers = {'Content-Type': 'application/json'}

app = Flask(__name__)
app.secret_key = 'CS50Final'

@app.route("/")
@login_required
def index():
    today = date.today()
    month = today.strftime("%m")
    query = "SELECT * FROM todo_{} WHERE date = ?".format(session['user'])
    sql = sqlite3.connect('database.db')
    cursor = sql.cursor()
    cursor.execute(query, (month,))
    row = cursor.fetchall()
    sql.close()
    todo = []
    for i in range (len(row)):
        todo.append(row[i][2])
    return render_template("index.html", k = len(row), todaytodo=todo)

#for calendar year 
@app.route('/toPy', methods=['POST','Get'])
def Py():
    #Getting the date value
    variable =  request.form['Thedate']
    start = 0
    digit = 0
    print(variable)
    #determind the value of the variable
    if int(variable) > 13:
        start = 1
        digit = 4 
    else:
        start = 6
        digit = 2
    #executing sql to retrieve the data
    sql = sqlite3.connect('database.db')
    cursor = sql.cursor()
    query = 'Select * from event_{} WHERE SUBSTR (Date, ?, ?) = ?'.format(session['user'])
    cursor.execute(query, (start, digit, variable))
    row = cursor.fetchall() #store the variable
    sql.close()
    if len(row) != 0:
        date = []
        event = []
        category = []
        print(row)
        print(len(row))
        for i in range(len(row)):
            date.append(row[i][0])
            event.append(row[i][1])
            category.append(row[i][3])
        return jsonify({'status': 'success', 'data': {'date': date, 'event': event, 'category': category, 'len': len(row) }})
    return jsonify({'message': 'Item sended successfully'}) 
    

@app.route("/calendar", methods=["POST",'GET'])
@login_required
def calendar():
    #getting the value from HTML
    if request.method == 'POST':
        event =  request.form.get("event_name")
        Thedate = request.form.get("datepicker")
        category = request.form.get("Category")
        #upload the data into sql
        sql = sqlite3.connect('database.db')
        cursor = sql.cursor()
        query = 'INSERT INTO event_{} (Date, Name, Category) VALUES (?,?,?)'.format(session['user'])
        cursor.execute(query,(Thedate,event, category))
        sql.commit()
        sql.close()
    return render_template("calendar.html")

@app.route("/calendar_month", methods=['POST',"GET"])  
@login_required
def cal_month():
    if request.method == 'POST':
        event =  request.form.get("event_name")
        Thedate = request.form.get("datepicker")
        category = request.form.get("Category")
        #upload the data into sql
        sql = sqlite3.connect('database.db')
        cursor = sql.cursor()
        query = 'INSERT INTO event_{} (Date, Name, Category) VALUES (?,?,?)'.format(session['user'])
        cursor.execute(query,(Thedate,event, category))
        sql.commit()
        sql.close()
    return render_template("calendar_month.html") 

@app.route("/calendar_year", methods=['POST','GET'])
@login_required
def cal_year():
    if request.method == 'POST':
        event =  request.form.get("event_name")
        Thedate = request.form.get("datepicker")
        category = request.form.get("Category")
        #upload the data into sql
        sql = sqlite3.connect('database.db')
        cursor = sql.cursor()
        query = 'INSERT INTO event_{} (Date, Name, Category) VALUES (?,?,?)'.format(session['user'])
        cursor.execute(query,(Thedate,event, category))
        sql.commit()
        sql.close()
    return render_template("calendar_year.html") 

@app.route('/new_task', methods=['POST']) 
def new_task():
    #getting the task from todo.html
    task = request.form['Task']
    month = request.form['month']
    #executing sql to store the new todo into database
    sql = sqlite3.connect('database.db')
    cursor = sql.cursor()
    query = 'INSERT INTO todo_{} (date, value) VALUES (?, ?)'.format(session['user'])
    cursor.execute(query,(month, task))
    sql.commit()
    sql.close()
    return jsonify({'message': 'Item sended successfully'}) 

#fetch the value from js andd deleting the value in database.db
@app.route('/delete_item', methods=['POST'])
def delete_item():
    label_value = request.form['labelValue']
    month = request.form['month']
    #deleting the items from database
    sql = sqlite3.connect('database.db')
    cursor = sql.cursor()
    query = 'DELETE FROM todo_{} WHERE date = ? AND value = ?'.format(session['user'])
    cursor.execute(query,(month, label_value))
    sql.commit()
    sql.close()
    return jsonify({'message': 'Item deleted successfully'})

#all the function are working just have to figure out how to pass the value to html
@app.route("/todo", methods=['POST','GET'])
@login_required
def todo():
    #getting the current month
    newTodo = None
    queryTodo = None
    now = datetime.now()
    month = now.strftime('%m')
    user = 'event_' + str(session['user'])
    #if request method == post change month with desire month
    if request.method == 'POST':
        month = request.form.get('month')
        newTodo = request.form.get('new_task')
    #performing sql to check what are the upcoming event
    if newTodo != None:
        queryTodo = 'INSERT INTO todo_{} (date, value) VALUE (?,?)'.format(session['user'])
    sql = sqlite3.connect('database.db')
    cursor = sql.cursor()
    query = 'SELECT * FROM {} WHERE SUBSTR (Date, 6,2) = ?'.format(user)
    cursor.execute(query,(str(month),))
    rows = cursor.fetchall()
    query2 = 'SELECT * FROM todo_{} WHERE date is ?'.format(session['user'])
    cursor.execute(query2,(str(month),))
    rowTodo = cursor.fetchall()
    if queryTodo != None:
        cursor.execute(queryTodo, (str(month), newTodo))
        sql.commit()
    i = list(rows)
    j = list(rowTodo)
    b = len(i) #b is working
    d = len(j)
    date = [None] * b
    name = [None] * b
    value = [None] * d
    for c in range (b):
        date[c] = i[c][0]
        name[c] = i[c][1]
    for e in range (d):
        value[e] = j[e][2]
    print(date)
    print(name)
    print(value)
    return render_template("todo.html", j=d,todo=value,k=b, date=date, list=name)

#providing the number that calculated through daily Q and A
@app.route("/report", methods = ['POST','GET'])
@login_required
def report():
    #getting the current month to make sure report displaying the current month data
    now = datetime.now()
    month = now.strftime('%m')
    #if the req method is post, change the month to the desire month
    if request.method == "POST":
        month = request.form.get('month')

    #with helpers.py retriving the data from each focus that stored in sql
    body = get_data('Body', str(month), session['user'])
    mind = get_data('Mind', str(month), session['user'])
    social = get_data('Social', str(month), session['user'])
    goal = get_data('Goal', str(month), session['user'])

    # Create a list of categories and values
    categories1 = body[0] #[0] for date
    values1 = body[1] #[1] for the value
    categories2 = mind[0]
    values2 = mind[1]
    categories3 = social[0]
    values3 = social[1]
    categories4 = goal[0]
    values4 = goal[1]

    #categories and values for the Summaries line chart
    x = body[0]
    y1 = body[1]
    y2 = mind[1]
    y3 = social[1]
    y4 = goal[1]

    # Create a list of trace objects for each category
    traces1 = []
    for category1, value1 in zip(categories1, values1):
        trace1 = go.Bar(
            x=[category1],
            y=[value1],
            name=category1
        )
        traces1.append(trace1)

    traces2 = []
    for category2, value2 in zip(categories2, values2):
        trace2 = go.Bar(
            x=[category2],
            y=[value2],
            name=category2
        )
        traces2.append(trace2)

    traces3 = []
    for category3, value3 in zip(categories3, values3):
        trace3 = go.Bar(
            x=[category3],
            y=[value3],
            name=category3
        )
        traces3.append(trace3)
        
    traces4 = []
    for category4, value4 in zip(categories4, values4):
        trace4 = go.Bar(
            x=[category4],
            y=[value4],
            name=category4
        )
        traces4.append(trace4)
    
    #the tracers for the line chart
    tracer1 = go.Scatter(x=x, y=y1, mode="lines", name="Body")
    tracer2 = go.Scatter(x=x, y=y2, mode="lines", name="Mind")
    tracer3 = go.Scatter(x=x, y=y3, mode="lines", name="Social")
    tracer4 = go.Scatter(x=x, y=y4, mode="lines", name="Goal")

    # Create the layout object
    layout1 = go.Layout(
        title='Body',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Value')
    )
    layout2 = go.Layout(
        title='Mind',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Value')
    )
    layout3 = go.Layout(
        title='Social',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Value')
    )
    layout4 = go.Layout(
        title='Goal',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Value')
    )
    #layout for the line chart
    layout = go.Layout(title='Summaries', xaxis = dict(title = 'Date'), yaxis = dict(title = "Value"))

    # Create the figure object
    fig1 = go.Figure(data=traces1, layout=layout1)
    fig2 = go.Figure(data=traces2, layout=layout2)
    fig3 = go.Figure(data=traces3, layout=layout3)
    fig4 = go.Figure(data=traces4, layout=layout4)
    fig = go.Figure(data=[tracer1, tracer2, tracer3, tracer4], layout=layout)

    # Convert the figure to JSON
    graphJSONB = fig1.to_json()
    graphJSONM = fig2.to_json()
    graphJSONS = fig3.to_json()
    graphJSONG = fig4.to_json()
    chart = fig.to_json()

    # Render the template and pass in the JSON data
    return render_template('report.html', graphJSONB=graphJSONB,graphJSONM=graphJSONM,graphJSONS=graphJSONS,graphJSONG=graphJSONG, Sum=chart)

@app.route("/profile", methods = ["POST","GET"])
@login_required
def profile():
    error_profile = None
    #running sql to pass a value to the user page
    sql = sqlite3.connect("database.db")
    cursor = sql.cursor()
    cursor.execute("SELECT * FROM user WHERE id = ?", (session['user'], ))
    row = cursor.fetchone()
    cursor.close()
    sql.close()
    username = row[2]
    age = row[6]
    occ = row[7]
    if request.method == "POST":
        #getting the inputed value from user
        username = request.form.get("username")
        age = request.form.get('age')
        occ = request.form.get('occupation')
        if not username or not age or not occ:
            error_profile = "all colum should be filled"
            return render_template("profile.html", username=username, age=age, occupation=occ, error_profile=error_profile)
        #performing sql again to check the inputed value with the database, only for username
        sql = sqlite3.connect("database.db")
        cursor = sql.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?",(username, ))
        row_1 = cursor.fetchone()
        cursor.close()
        sql.close()
        if row_1 is not None and row_1[0] != session['user']:
            error_profile = 'Username is taken'
            return render_template("profile.html", username=username, age=age, occupation=occ, error_profile=error_profile)
        #doing another sql session to put the user    
        sql = sqlite3.connect('database.db')
        cursor = sql.cursor()
        cursor.execute("UPDATE user SET username = ?, age = ?, occupation = ? WHERE id = ?",(username,age,occ, session['user']))
        sql.commit()
        cursor.execute("SELECT * FROM user WHERE username = ?",(username,))
        row_2 = cursor.fetchone()
        print(row_2)
        cursor.close()
        sql.close()
        #send a confirmation text and output the latest profile
        confirm = "Profile successfully changed"
        print("POST")
        return render_template("profile.html", username=row_2[2], age=row_2[6], occupation=row_2[7], confirm=confirm)        
    else: 
        print("get")
        return render_template("profile.html", username=username, age=age, occupation=occ)

#checking the password and chang it if the user click the update password btn
#user could ve directed to this page if they pass the requirements in forget_pass page. 
@app.route("/password", methods=["POST","GET"])
@login_required
def password():
    error = None
    update = None
    if request.method == "POST":
        #getting the value of the inputs
        pass_old = request.form.get("password")
        new_pass = request.form.get("new_pass")
        retype_new_pass = request.form.get("retype_new_pass")
        #making sure all input are inputed
        if not new_pass:
            error = 'New password colum is empty'
            return render_template("password.html", error=error,password=pass_old)
        if not retype_new_pass:
            error = 'Retype new password colum is empty'
            return render_template("password.html", error=error,password=pass_old)
        if not pass_old:
            error = 'Current password is required'
            return render_template("password.html", error=error)
        #checking weather the new pass and retype are the same
        if new_pass != retype_new_pass:
            error = "New password do not match"
            return render_template("password.html", error=error,password=pass_old)
        #to check wether they came from forget pass page or index
        if pass_old == 'protected':
            pass_old = session.get('password') #haven't check weather the session[pass] is working
        else:
            pass_old = generate_password_hash(pass_old)
        #executing sql line to check the password and change it.
        sql = sqlite3.connect('database.db')
        cursor = sql.cursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (session['user'], ))
        output = cursor.fetchone()
        cursor.close()
        sql.close()
        #checking the inputed current password with database using werkzeug.security 
        if pass_old != output[3]:
            error = 'Current password is wrong'
            return render_template('password.html', error=error)
        #inputing the new password to the database
        sql = sqlite3.connect('database.db')
        cursor = sql.cursor()
        cursor.execute('UPDATE user SET password = ? WHERE id = ?', (pass_old, session['user']))
        sql.commit()
        cursor.close()
        sql.close()
        #send a text to let the user know that password is updated
        update = 'Password has been updated'
        return render_template('password.html', update=update)
    else: 
        return render_template("password.html",error=error)

#fetch a question from database.db and fetch the value of it and store it in database again.
#Might need to do a research about how to count and determind the value of it. 
@app.route("/q_and_a", methods=["POST", "GET"])
@login_required
def q_and_a():
    #executing a database to check weather the QandA is filled 
    note = None
    user = "User_" + str(session.get('user'))
    current_date = date.today()
    sql = sqlite3.connect('database.db')
    cursor = sql.cursor()
    query = 'SELECT * FROM {} WHERE Date is ?'.format(user)
    cursor.execute(query,(current_date,))
    row = cursor.fetchone()
    cursor.close()
    sql.close()
    if row :
        #if its filled will be directed to filled.html 
        return render_template('filled.html')
    #retrief the questions
    Q1 = get_question('body', 4)
    Q2 = get_question('body', 3)
    Q3 = get_question('mind', 4)
    Q4 = get_question('mind', 5)
    Q5 = get_question('social', 4)
    Q6 = get_question('social', 3)
    Q7 = get_question('goal', 4)
    Q8 = get_question('goal', 3)
    if request.method == "POST":
        print("app.py 183")
        #getting the value that inputed
        q1 = (request.form.get("Q1"))
        q2 = (request.form.get("Q2"))
        q3 = (request.form.get("Q3"))
        q4 = (request.form.get("Q4"))
        q5 = (request.form.get("Q5"))
        q6 = (request.form.get("Q6"))
        q7 = (request.form.get("Q7"))
        q8 = (request.form.get("Q8"))
        #making sure all the questions are filled
        if q1 is None or q2 is None or q3 is None or q4 is None or q5 is None or q6 is None or q7 is None or q8 is None:
            note = "All questions must be filled"
            return render_template("q_and_a.html", note=note, Q1 = Q1, Q2 = Q2, Q3 = Q3, Q4 = Q4, Q5 = Q5, Q6 = Q6, Q7 = Q7, Q8 = Q8)
        #convert str into int
        q1 = int(q1)
        q2 = int(q2)
        q3 = int(q3)
        q4 = int(q4)
        q5 = int(q5)
        q6 = int(q6)
        q7 = int(q7)
        q8 = int(q8)
        #then calculate for each focus
        #will have to do a better calculation later on.
        body = q1 + q2 
        mind = q3 + q4
        social = q5 + q6
        goal = q7 + q8
        #execute sql function to store the focus values into database.db
        #succedfully inputing all the value into sql
        sql=sqlite3.connect("database.db")
        cursor = sql.cursor()
        query1 = "INSERT INTO {} (Date, Body, Mind, Social, Goal) VALUES (?,?,?,?,?)".format(user)
        cursor.execute(query1, (current_date,body,mind,social,goal))
        query2 = "SELECT * FROM {}".format(user)
        cursor.execute(query2)
        Row = cursor.fetchone()
        print(Row)
        sql.commit()
        print(user)
        cursor.close()
        sql.close()
        #will be directed to filled once it finished.
        return render_template("filled.html")
    else: 
        return render_template("q_and_a.html",Q1 = Q1, Q2 = Q2, Q3 = Q3, Q4 = Q4, Q5 = Q5, Q6 = Q6, Q7 = Q7, Q8 = Q8)


@app.route("/logout")
def logout():
    #clear the session and directing to logout page with options
    session.clear()
    return render_template("logout.html")

#Checking the inputed value with database
@app.route("/login", methods=["POST","GET"])
def login():
    error_login = None
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "POST":
        #Making sure all colum is filled
        if not username:
            error_login = "Please input your username"
            return render_template("login.html", error_login = error_login)
        if not password:
            error_login = "Please input your password"
            return render_template("login.html", error_login= error_login)
        #performing sql to check the username with the database
        sql = sqlite3.connect("database.db")
        cursor = sql.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        row = cursor.fetchone()
        print(row)
        cursor.close()
        sql.close()
        #if username is not found, will return error 
        if row == None:
            error_login = "Username is not found try to signup instead"
            return render_template("login.html", error_login=error_login)
        check = check_password_hash(row[3], password)
        if not check:
            error_login = "Wrong password"
            return render_template("login.html", error_login=error_login)
        #if the user meet all requirement, session will be made and then directing to the index page
        session["user"] = row[0]
        return redirect('/')
    else: 
        return render_template("login.html")

#Sign up form, to check with the system to make sure there is no double username or email. 
#Collecting user details and put it in session, then send it to code_checking. 
@app.route("/signup", methods= ["POST", "GET"])
def singup():
    #Initialize the flask value and set it to none
    error_email = None
    error_user = None
    error_pass = None
    error_pass2 = None
    error_gender = None
    error_other_gender = None
    error_age = None
    error_occ = None
    if request.method == "POST":
        #Getting the value of the needed forms
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        retype_password = request.form.get("retype-password")
        gender = request.form.get("gender")
        other = request.form.get("other_gender")
        age = request.form.get("age")
        occupation = request.form.get("occupation")

        #Checking all form are filled and meet the requirement
        if not email:
            error_email = "Please input your email"
        #making sure the email is not reqister to other account
        val_email = 'name'
        check = search(val_email, email)
        if check is not None:
            error_email = "Email is taken, try to sign in"
        
        if not username:
            error_user = "Please input your username"
        
        #Checking weather the user name is taken or not
        user = 'username'
        check2 = search(user, username)
        if check2 is not None:
            error_user = "username is taken"
        #Checking all form are filled
        if not password:
            error_pass = "Please input your password"
        if not retype_password:
            error_pass2 = "Please retype-your password"
        #checking weather the passwords are match 
        if password != retype_password:
            error_pass = "Password do not match"
            error_pass2 = "Password do not match"
        if not gender:
            error_gender = "Please select your gender"
        #making sure the user fill the other for if they categories as other in the gender. 
        if gender == 'O' and not other:
             error_other_gender = "Please input your gender"
        else:
            other = 'Binary'
        #Checking all form are filled
        if not age:
            error_age = "Please input your age"
        if not occupation:
            error_occ = "Please select your occupation" 
        #make sure all the form are filled
        if not all(variable is None for variable in [error_user, error_email, error_age, error_other_gender,error_gender, error_occ, error_pass, error_pass2]):
            return render_template("signup.html", error_email=error_email, error_user=error_user, error_pass=error_pass, error_pass2=error_pass2, error_gender=error_gender,error_other_gender=error_other_gender,error_occ=error_occ, error_age=error_age)
        #set all variables into session
        session['email'] = email
        session['username'] = username 
        session['password'] = password 
        session['gender'] = gender 
        session['other'] = other 
        session['age'] = age 
        session['occupation'] = occupation          
        return redirect(url_for("code_checking"))
    else:
        return render_template("signup.html", 
                               error_email=error_email, error_user=error_user, error_pass=error_pass, error_pass2=error_pass2, error_gender=error_gender, error_other_gender=error_other_gender, error_age=error_age, error_occ=error_occ)

@app.route("/forget_pass", methods=["POST","GET"])
def forget_pass():
    error = None
    if request.method == "POST":
        #getting the email
        email = request.form.get('email')
        print(email)
        #checking weather the email is valid user
        sql = sqlite3.connect("database.db")
        cursor = sql.cursor()
        cursor.execute ('SELECT * FROM user where name = ?',(email,))
        row = cursor.fetchone()
        cursor.close()
        sql.close()
        #If the email is not reqistered in the sytem, will send an error code and sugesting to signup
        if row == None:
            error = "Email is not found, Do you want to Sign Up instead?"
            return render_template ("forget_pass.html", error=error)
        #put the email in session
        session['email'] = email
        return redirect(url_for("forget_pass_code_checking"))
    else:
        return render_template("forget_pass.html", error=error)
    
@app.route("/forget_pass_code_checking", methods=["POST","GET"])    
def forget_pass_code_checking():
    error = None
    error = session.get('error')
    #getting the email, 6 digit code and send it to the user email
    email = session.get("email")
    code = random_string
    confirmation = templates(email,code)
    if request.method == "POST":
        #make sure email sended
        if confirmation == False:
            confirmation = templates(email, code)
        #Initialize the variables
        match = 0 
        form = []
        #place code into list
        code_list = list(code)
        #getting the value from form and store it in list, no case sensitive
        for j in range(1,7):
            loop = str(j)
            value = request.form.get(loop)
            form.append(value.upper())
        #checking the code that we sended and the inputed are match
        for i in range(6):
            if form[i] == code_list[i]:
                match += 1
            else:
                match += 0
        #if not match make sure it goes back
        if match != 6:
            error = "Code is not Match"
            return render_template("forget_pass_code_checking.html", error=error)
        #Putting the user id to the session before directing to password.
        sql = sqlite3.connect('database.db')
        cursor = sql.cursor()
        cursor.execute("SELECT * FROM user where name = ?",(email,))
        row = cursor.fetchone()
        cursor.close()
        sql.close()
        #clear the session to make sure no memory leak
        session.clear()
        session['user'] = row[0]
        session['password'] = row[3]
        #sending old password value to the page
        password = "protected"
        print(row)
        #redirecting to password page to ask the user to change the password. 
        return render_template("password.html", password=password)
    else:
        return render_template("forget_pass_code_checking.html", error=error)

#for the resend code btn in forget pass code checking page
@app.route("/resend_code_fp", methods=["POST"])
def resend_code_fp():
    if request.method == 'POST':
        error = "Code Sended, Check your email"
        session['error'] = error
        return redirect(url_for("forget_pass_code_checking"))
    else:
        error = "Code Sended, Check your email"
        session['error'] = error
        return render_template(url_for("forget_pass_code_checking"))
        
        
#/code_checking, sending the 6 digit code, checking it and login user using session
@app.route("/code_checking", methods=["POST", "GET"])
def code_checking():
    error = None
    error = session.get("error")
    #fetch the variable in session 
    email = session.get("email")
    password = session.get("password")
    username = session.get("username")
    gender = session.get("gender")
    other = session.get("other")
    age = session.get("age")
    occupation = session.get("occupation")
    code = random_string
    confirmation = templates(email,code)
    if request.method == "POST":
        #make sure email sended
        if confirmation == False:
            confirmation = templates(email, code)
        #Initialize the variables
        match = 0 
        form = []
        #place code into list
        code_list = list(code)
        #getting the value from form and store it in list, no case sensitive
        for j in range(1,7):
            loop = str(j)
            value = request.form.get(loop)
            form.append(value.upper())
        #checking the code that we sended and the inputed are match
        for i in range(6):
            if form[i] == code_list[i]:
                match += 1
            else:
                match += 0
        #if not match make sure it goes back
        if match != 6:
            error = "Code is not Match"
            return render_template("code_checking.html", error=error)
        #generating hash code for the password
        pass_hash = generate_password_hash(password)
        #Input the user's data into database. 
        sql = sqlite3.connect("database.db")
        cursor = sql.cursor()
        cursor.execute('INSERT INTO user (name, username, password, gender, other_gender, age, occupation)VALUES (?,?,?,?,?,?,?)',(email,username,pass_hash,gender,other,age,occupation))
        #fetch the user id that had been inputed
        cursor.execute('SELECT * FROM user WHERE username = ?',(username,))
        row = cursor.fetchone()
        sql.commit()
        id = 'User_' + str(row[0])
        todo = 'todo_'+str(row[0])
        event = 'event_'+str(row[0])
        print("line 488")
        query = 'CREATE TABLE {} (Date TEXT, Body INTEGER NOT NULL, Mind INTEGER NOT NULL, Social INTEGER NOT NULL, Goal INTEGER NOT NULL)'.format(id)
        #create a table for all new user
        cursor.execute(query)
        sql.commit()
        query2 = 'CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, value TEXT NOT NULL)'.format(todo)
        cursor.execute(query2)
        sql.commit()
        query3 = '''CREATE TABLE IF NOT EXISTS {} (
            Date TEXT NOT NULL,
            Name TEXT NOT NULL, 
            Description TEXT, 
            Category CHAR(1) NOT NULL CHECK(Category IN ('B','M','S','G'))
            )'''.format(event)
        cursor.execute(query3)
        sql.commit()
        cursor.close()
        sql.close()
        session.clear()
        #using session to store the id and directing to index page. 
        session['user'] = row[0]
        #create a table for all new user
        return redirect("/")
    else: 
        return render_template("code_checking.html",error=error)

#for the resend code btn in code checking page
@app.route("/resend_code", methods=["POST"])
def resend_code():
    if request.method == 'POST':
        error = "Code Sended, Check your email"
        session['error'] = error
        return redirect(url_for("code_checking"))
    else:
        error = "Code Sended, Check your email"
        session['error'] = error
        return render_template(url_for("code_checking"))
