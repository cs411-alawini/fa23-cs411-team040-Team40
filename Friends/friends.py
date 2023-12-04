from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from db import pool

friends = Blueprint('friends', __name__, url_prefix='/friends')

@friends.route('/', methods=["GET", "POST"])
def add_friend():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()
    if request.method == "GET":
        cursor.execute("SELECT Users.uid, username FROM Friends join Users on friendID = Users.uid WHERE Friends.uid = %s", (userid,))
        friends = list(cursor.fetchall())
        connection.commit()
        return render_template('friends.html', friends=friends)


    friendname = request.form['friendname']
    cursor.execute("SELECT uid FROM Users WHERE username = %s", friendname)
    friendid = cursor.fetchall()
    if friendid == ():
        flash('User does not exist')
        return redirect(url_for('add_friend', methods=["GET"]))
    elif friendid[0] == userid:
        flash('Cannot add yourself as a friend')
        return redirect(url_for('add_friend', methods=["GET"]))
    else:
        cursor.execute("INSERT INTO Friends (uid, friendid) VALUES (%s, %s)", (userid, friendid))
        connection.commit()
        flash('Successfully added friend')
        return redirect(url_for('add_friend', methods=["GET"]))


@friends.route('/remove', methods=["POST"])
def remove_friend():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    friendid = request.form['friendid']
    cursor.execute("SELECT username FROM Users WHERE uid = %s", friendid)
    friendname = cursor.fetchall()[0][0]

    cursor.execute("DELETE FROM Friends WHERE uid = %s AND friendid = %s", (userid, friendid))
    connection.commit()
    flash(f'Successfully removed {friendname} as a friend')
    return redirect(url_for('add_friend', methods=["GET"]))

@friends.route('/list', methods=["GET"])
def list_friends_games():
   connection = pool.raw_connection() 
    cursor = connection.cursor()
    friendid = request.args.get("friendid")

    cursor.execute("Select title, link, introduction FROM Games NATURAL JOIN Likes WHERE uid = %s", friendid)
    games_list = list(cursor.fetchall())

    cursor.execute("SELECT title, link, introduction FROM Games NATURAL JOIN Reviews WHERE uid = %s", friendid)
    rec_list = list(cursor.fetchall())
    games_list.extend(rec_list)
    connection.commit()
    print(games_list)
    return render_template("dispaly_games.html", games_list=games_list)




