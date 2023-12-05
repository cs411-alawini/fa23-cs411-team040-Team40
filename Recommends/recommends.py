from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from db import pool

recommends_bp = Blueprint('recommends', __name__, url_prefix='/recommends')
# Recommend games based on the user's likes and the user's friends' likes
@recommends_bp.route('/', methods=['GET'])
def recommend_games():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    userid = session['userid']    
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
        "SELECT gid, title, link, introduction FROM Games WHERE gid IN %s",
        (tuple(all_liked_games),)
    )
    recommended_games = list(cursor.fetchall())
    return render_template('games.html', games_list = recommended_games)