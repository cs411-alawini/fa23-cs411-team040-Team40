from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from app import pool

friends = Blueprint('friends', __name__, url_prefix='/friends')

@friends.route('/friends', methods=["GET", "POST"])
def add_friend():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()
    if request.method == "Get":
        cursor.execute("SELECT * FROM friends WHERE userid = %s", (userid,))
        friends = cursor.fetchall()
        return render_template('friends.html', friends=friends)
    
    elif request.method == "POST":
        friendname = request.form['friendname']
        friendid = cursor.execute("SELECT userid FROM users WHERE username = %s", (friendname,))
        if friendid == None:
            flash('User does not exist')
            return redirect(url_for('friends', methods=["GET"]))
        elif friendid == userid:
            flash('Cannot add yourself as a friend')
            return redirect(url_for('friends', methods=["GET"]))
        else:
            cursor.execute("INSERT INTO friends (userid, friendid) VALUES (%s, %s)", (userid, friendid))
            connection.commit()
            flash('Successfully added friend')
            return redirect(url_for('friends', methods=["GET"]))


@friends.route('/friends', methods=["POST"])
def remove_friend():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    friendname = request.form['friendname']
    friendid = cursor.execute("SELECT userid FROM users WHERE username = %s", (friendname,))

    cursor.execute("DELETE FROM friends WHERE userid = %s AND friendid = %s", (userid, friendid))
    connection.commit()
    flash('Successfully removed %s as a friend', friendname)
    return redirect(url_for('friends', methods=["GET"]))




