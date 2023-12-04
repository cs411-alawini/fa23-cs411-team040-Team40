from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from app import pool

likes = Blueprint('likes', __name__, url_prefix='/likes')
@likes.route('/', methods=['POST'])
def like_game():
    if 'username' not in session:
        return redirect(url_for('login.login')) #########

    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    gamename = request.form['gamename']
    gameid = cursor.execute("SELECT gid FROM Games WHERE title = %s", (gamename,))

    # Fetch user using raw SQL query
    cursor.execute("SELECT * FROM Users WHERE uid = %s", (userid,))
    user = cursor.fetchone()

    if not user:
        flash("User not found.", 'error')
        return redirect(url_for('gamesearch'))

    # Fetch game using raw SQL query
    cursor.execute("SELECT * FROM Games WHERE gid = %s", (gameid,))
    game = cursor.fetchone()

    if not game:
        flash("Game not found.", 'error')
        return redirect(url_for('gamesearch'))

    # Check if the user already likes the game using raw SQL query
    cursor.execute("SELECT * FROM Likes WHERE uid = %s AND gid = %s", (userid, gameid))
    existing_like = cursor.fetchone()

    if existing_like:
        flash("You already liked this game.", 'info')
        return redirect(url_for('gamesearch'))

    # Add a like for the user and game using raw SQL query
    cursor.execute("INSERT INTO Likes (uid, gid) VALUES (%s, %s)", (userid, gameid))
    connection.commit()
    flash("You liked the game!", 'success')

    return redirect(url_for('gamesearch'))


