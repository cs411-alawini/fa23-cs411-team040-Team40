from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from db import pool

likes_bp = Blueprint('likes', __name__, url_prefix='/likes')
@likes_bp.route('/', methods=['GET', 'POST'])
def like_game():
    session['userid'] = 1
    session['username'] = 'test'
    if 'username' not in session:
        return redirect(url_for('login.login'))

    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()
    
    if request.method == "GET":
        cursor.execute("SELECT gid, title, link, introduction from Likes natural join Games where uid = %s", (userid,))
        like_lists = list(cursor.fetchall())
        return render_template('game.html', game_list = like_lists)
    
    gid = request.form['gid']
    if gid == ():
        flash('Game does not exist')
        return redirect(url_for('game.html', methods=["GET"]))
    else:
        cursor.execute("INSERT INTO Likes (uid, gid) VALUES (%s, %s)", (userid, gid))
        connection.commit()
        flash('Successfully added game')
        return redirect(url_for('game.html', methods=["GET"]))

@likes_bp.route('/remove', methods=["POST"])
def remove_game():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    gid = request.form['gid']
    cursor.execute("DELETE from Likes WHERE uid=%s and gid=%s", (userid, gid))
    connection.commit()
    flash(f'Successfully removed game')
    return redirect(url_for('game.html', methods=["GET"]))


