#for flask
from flask import Flask, flash, redirect, render_template, request, session
#csv and random for get_question function
import csv
import random
import sqlite3 #sqlite for the database
#smtplib for sending email template
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
#to generating hash password
from werkzeug.security import check_password_hash, generate_password_hash
#for @login request to wrap the user, to make sure it not leek
from functools import wraps



app = Flask(__name__)

# Generating random code from SQLite 
# Establish a connection to the SQLite database
conn = sqlite3.connect('random.db')
# Create a cursor object
cursor = conn.cursor()
# Execute the recursive SQL query
cursor.execute("""
    WITH RECURSIVE RandomString AS (
        SELECT CHAR(65 + ABS(RANDOM()) % 26) ||
               CHAR(65 + ABS(RANDOM()) % 26) ||
               CHAR(48 + ABS(RANDOM()) % 10) ||
               CHAR(48 + ABS(RANDOM()) % 10) ||
               CHAR(65 + ABS(RANDOM()) % 26) ||
               CHAR(65 + ABS(RANDOM()) % 26) AS RandomString
        UNION
        SELECT RandomString || CHAR(65 + ABS(RANDOM()) % 26)
        FROM RandomString
        WHERE LENGTH(RandomString) < 6
    )
    SELECT RandomString FROM RandomString LIMIT 1;
""")
# Fetch the result (assuming only one row is returned)
result = cursor.fetchone()
# Extract the value from the result tuple
random_string = result[0] if result else None
# Close the cursor and connection
cursor.close()
conn.close()

#a function for searching value of a data in database. 
#object is what you looking for and item, stand for the item in the object.
def search(object, item):
    database = sqlite3.connect('database.db')
    sql = database.cursor()
    sql.execute(f'SELECT * FROM user WHERE {object} = ?', (item,))
    output = sql.fetchone() 
    final_output = output[0] if output else None
    sql.close()
    database.close()
    # Correct way to call the search function
    return final_output

#Sending email templates to send the 6 digit code for checking code page
def templates(email, code):
    try:
        sender = "bsella2000@gmail.com"
        sender_pass = "cbqa qgri ybxu bxio"
        subject = "6 Digit Code"
        code = code
        #the templates for the email
        html_template = f'''

        <html>
            <body>
            <h2>Welcome to ShinEra ✨</h2>
            <p>This is your 6 Digit Code.</p>
            <p> {code} <p>
            <p>Hope you have a shiney day a head!<p>
            </body>
        </html>

        '''

        # Create a multipart message
        message=MIMEMultipart()
        message["From"] = sender
        message["To"] = email
        message["Subject"] = subject

        # Add HTML template to the message
        message.attach(MIMEText(html_template,"html"))
        # Setup the SMTP server
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465 ) 
        # Login into SMTP
        smtp_server.login(sender,sender_pass)
        # Sending the email
        smtp_server.sendmail(sender,email, message.as_string()) 
        #quit the server after
        smtp_server.quit()
        return True
    except Exception as e:
        return False
    
#login the user using session and checking it
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#In order to get a random value but still maintaining the correct range of question in csv 
def get_random(value):
    if value == 'body':
        return random.sample(range(2, 17), 1)[0]
    elif value == 'mind':
        return random.sample(range(18, 32), 1)[0]
    elif value == 'goal':
        return random.sample(range(33, 53), 1)[0]
    elif value == 'social':
        return random.sample(range(54, 77), 1)[0]
    else:
        raise ValueError("Invalid value parameter. Please specify 'body', 'mind', 'goal', or 'social'.")

#getting the questions from csv file
def get_question(focus, weight):
    Q = None
    i = 1
    while Q is None:
        # Opening a csv file to fetch the questions and value 
        csv_file_path = "question.csv"
        with open(csv_file_path, newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            f = get_random(focus)
            w = int(weight)       
            # Initialize variables to store the questions
            for row in csv_reader:
                if i == f: #if the row is match with the random that we set
                    if int(row[1]) == w: #make sure the weight of the questions also match with the desire Q and A
                        Q = row[2]
                        break  # Exit the loop after finding the desired row
                    else:
                        i = 1 
                        break 
                i += 1 #will keep looping until row meet the desire row
    #returning the Q which is the question
    return Q

#getting the value and date from sql to display it in the report
def get_data(focus, month, user):
    user_id = 'User_' + str(user)
    if focus == 'Body':
        focus = 1
    elif focus == 'Mind':
        focus = 2
    elif focus == 'Social':
        focus = 3
    elif focus == 'Goal':
        focus = 4
    #executing sql to retvite the data in it
    sql = sqlite3.connect('database.db')
    cursor = sql.cursor()
    query = 'SELECT * FROM {} WHERE SUBSTR(Date, 6, 2) is ?'.format(user_id) #using qeury as parameter to execute the sql
    cursor.execute(query, (month,))
    row = cursor.fetchall()
    cursor.close()
    sql.close()
    #initialise the arrays
    date = []
    value = []
    for i in range(len(row)):
        date.append(row[i][0][-2:]) #to get the date only         
        value.append(row[i][focus])
    #returning the date and value back to app.py
    return date, value

