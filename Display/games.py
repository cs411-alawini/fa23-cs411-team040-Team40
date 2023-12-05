from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from db import pool

games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.route('/', methods=['GET', 'POST'])
def games():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()
    if request.method == "GET":
        friendid = request.args.get("friendid")

        cursor.execute("Select gid, title, link, introduction FROM Games NATURAL JOIN Likes WHERE uid = %s", friendid)
        games_list = list(cursor.fetchall())

        cursor.execute("SELECT gid, title, link, introduction FROM Games NATURAL JOIN Reviews WHERE uid = %s", friendid)
        rec_list = list(cursor.fetchall())
        games_list.extend(rec_list)
        connection.commit()
        return render_template("games.html", games_list=games_list)

    gid = request.form['gid']
    session['gid'] = gid
    return redirect(url_for("games.game"))

@games_bp.route('/game', methods=['GET'])
def game():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    gid = session['gid']
    cursor.execute("SELECT username, rating, content FROM Reviews NATURAL JOIN Users WHERE gid = %s limit 5", (gid,))
    existing_reviews = list(cursor.fetchall())
    cursor.execute("SELECT gid, title, link, introduction FROM Games WHERE gid = %s", (gid,))
    game_info = cursor.fetchone()
    print(game_info)
    cursor.execute("SELECT * FROM Likes WHERE uid = %s AND gid = %s", (userid, gid))
    current_user_likes = cursor.fetchall()
    connection.commit()
    if current_user_likes == ():
        current_user_likes = False
    else:
        current_user_likes = True
    return render_template("game.html", game_info=game_info, existing_reviews=existing_reviews, current_user_likes=current_user_likes)