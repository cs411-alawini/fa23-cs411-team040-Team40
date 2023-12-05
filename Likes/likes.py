from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from db import pool

likes_bp = Blueprint('likes', __name__, url_prefix='/likes')
@likes_bp.route('/', methods=['GET', 'POST'])
def like_game():
    session['userid'] = 1
    session['username'] = 'test'
    if 'username' not in session:
        return redirect(url_for('login.login')) #########

    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT gid from Likes where uid = %s", (userid,))
    gids = cursor.fetchall()
    cursor.execute("SELECT title from Games where gid in %s", (gids,))
    game_titles = [game[0] for game in list(cursor.fetchall())]
    if request.method == "GET":
        return render_template('favorites.html', favorites=game_titles)
    gamename = request.form['gamename']
    cursor.execute("SELECT gid FROM Games WHERE title = %s", (gamename,))
    gid = cursor.fetchone()[0]
    if gid == ():
        flash('Game does not exist')
        return redirect(url_for('likes.like_game', methods=["GET"]))
    elif gid in gids:
        flash('Game Already Favorited')
        return redirect(url_for('likes.like_game', methods=["GET"]))
    else:
        cursor.execute("INSERT INTO Likes (uid, gid) VALUES (%s, %s)", (userid, gid))
        connection.commit()
        flash('Successfully added Game')
        return redirect(url_for('likes.like_game', methods=["GET"]))

@likes_bp.route('/remove', methods=["POST"])
def remove_game():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    game_title = request.form['game_title']
    cursor.execute("Select gid from Games where title = %s", game_title)
    gid = cursor.fetchone()[0]
    cursor.execute("DELETE from Likes WHERE uid=%s and gid=%s", (userid, gid))
    connection.commit()
    flash(f'Successfully unfavorited {game_title}')
    return redirect(url_for('likes.like_game', methods=["GET"]))


