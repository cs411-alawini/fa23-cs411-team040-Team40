from flask import Blueprint
from app import app, request, sqlalchemy, flash, redirect, session, url_for, render_template, pool
login = Blueprint('login', __name__, url_prefix='/login')
@login.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        query = f"SELECT count(*) FROM Users WHERE username='{username}' AND password='{password}'"
        #Verify username & password match in Database
        with pool.connect() as db_conn:
            results = db_conn.execute(sqlalchemy.text(query)).fetchall()
            uid = db_conn.execute(sqlalchemy.text(f"select uid from Users where username='{username}' and password='{password}'")).fetchall()[0][0]

        #Redirect back to login if no user found
        if results[0][0] == 0:
            flash("Incorrect Username or Password, please try again or signup for an account", 'error')
            return redirect(url_for('login'))

        #Using sessions so that user can later have personalized page
        session['username'] = username
        session['uid'] = uid

        return redirect(url_for('gamesearch'))
    
    return render_template("login.html")


@login.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        # Verify username is unique and add user to the database
        # https://justinmatters.co.uk/wp/using-sqlalchemy-to-run-sql-procedures/ 
        username = request.form["username"]
        password = request.form["password"]

        # Adding user by calling stored procedure
        try:
            with pool.connect() as db_conn:
                numUsers = db_conn.execute(sqlalchemy.text("select max(uid) from Users")).fetchall()[0][0] + 1
                db_conn.execute(sqlalchemy.text(f"insert into Users (uid, username, password) values ({numUsers}, '{username}', '{password}')"))
                # commit transaction (SQLAlchemy v2.X.X is commit as you go)
                db_conn.commit()
        except:
            flash(f"{username} already has an account, login or create a unique username", 'error')
            return redirect(url_for('signup'))
        
        #Adding username to session
        session['username'] = username
        session['uid'] = numUsers

        return redirect(url_for('gamesearch'))
    
    return render_template("signup.html")
