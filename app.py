from flask import Flask, render_template, jsonify, redirect, request, url_for, flash, session, Blueprint
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
# from db import pool

app = Flask(__name__)
app.secret_key = 'team40'



# initialize Connector object
# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    connector = Connector()
    conn: pymysql.connections.Connection = connector.connect(
        "cs-411-team:us-central1:myinstance",
        "pymysql",
        user="root",
        password="team40",
        db="steam"
    )
    return conn


# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)
"""test friends page and done"""
# @app.route('/', methods=["GET", "POST"])
# def add_friend():
#     # if 'username' not in session:
#         # return redirect(url_for('login.login'))
#         # print("not logged in")
#     userid = 1
#     connection = pool.raw_connection()
#     cursor = connection.cursor()
#     if request.method == "GET":
#         cursor.execute("SELECT Users.uid, username FROM Friends join Users on friendID = Users.uid WHERE Friends.uid = %s", (userid,))
#         friends = list(cursor.fetchall())
#         connection.commit()
#         return render_template('friends.html', friends=friends)


#     friendname = request.form['friendname']
#     cursor.execute("SELECT uid FROM Users WHERE username = %s", friendname)
#     friendid = cursor.fetchall()
#     if friendid == ():
#         flash('User does not exist')
#         return redirect(url_for('add_friend', methods=["GET"]))
#     elif friendid[0] == userid:
#         flash('Cannot add yourself as a friend')
#         return redirect(url_for('add_friend', methods=["GET"]))
#     else:
#         cursor.execute("INSERT INTO Friends (uid, friendid) VALUES (%s, %s)", (userid, friendid))
#         connection.commit()
#         flash('Successfully added friend')
#         return redirect(url_for('add_friend', methods=["GET"]))


# @app.route('/friends/remove', methods=["POST"])
# def remove_friend():
#     # if 'username' not in session:
#     #     return redirect(url_for('login.login'))
#     userid = 1
#     connection = pool.raw_connection()
#     cursor = connection.cursor()

#     friendid = request.form['friendid']
#     cursor.execute("SELECT username FROM Users WHERE uid = %s", friendid)
#     friendname = cursor.fetchall()[0][0]

#     cursor.execute("DELETE FROM Friends WHERE uid = %s AND friendid = %s", (userid, friendid))
#     connection.commit()
#     flash(f'Successfully removed {friendname} as a friend')
#     return redirect(url_for('add_friend', methods=["GET"]))

# @app.route('/friends/list', methods=["GET"])
# def list_friends_games():
#     connection = pool.raw_connection() 
#     cursor = connection.cursor()
#     friendid = request.args.get("friendid")

#     cursor.execute("Select title, link, introduction FROM Games NATURAL JOIN Likes WHERE uid = %s", friendid)
#     games_list = list(cursor.fetchall())

#     cursor.execute("SELECT title, link, introduction FROM Games NATURAL JOIN Reviews WHERE uid = %s", friendid)
#     rec_list = list(cursor.fetchall())
#     games_list.extend(rec_list)
#     connection.commit()
#     print(games_list)
#     return render_template("dispaly_games.html", games_list=games_list)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)