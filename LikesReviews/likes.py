from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from app import pool

@likesreviews.route('/likes', methods=['POST'])
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


# Recommend games based on the user's likes and the user's friends' likes
def recommend_games(userid):
    connection = pool.raw_connection()
    cursor = connection.cursor()

    # Fetch the games liked by the user
    cursor.execute("SELECT gid FROM Likes WHERE uid = %s", (userid,))
    user_liked_games = [row[0] for row in cursor.fetchall()]

    # Fetch the games liked by the user's friends
    friends_liked_games = []
    cursor.execute("SELECT friendid FROM Friends WHERE uid = %s", (userid,))
    friend_ids = [row[0] for row in cursor.fetchall()]

    for friend_id in friend_ids:
        cursor.execute("SELECT gid FROM Likes WHERE uid = %s", (friend_id,))
        friends_liked_games.extend([row[0] for row in cursor.fetchall()])

    # Combine user's and friends' liked games and remove duplicates
    all_liked_games = set(user_liked_games + friends_liked_games)

    # Fetch game details based on the liked game IDs
    cursor.execute(
        "SELECT title, link, genre, rating, content FROM Games NATURAL JOIN Reviews WHERE gid IN %s ORDER BY rating DESC",
        (tuple(all_liked_games),)
    )
    recommended_games = cursor.fetchall()


    return recommended_games