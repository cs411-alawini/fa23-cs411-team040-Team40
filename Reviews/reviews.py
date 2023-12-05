from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from db import pool

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')
@reviews_bp.route('/', methods=['GET', 'POST'])
def review_game():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    if request.method == "GET":
        cursor.execute("SELECT gid, title, rating, content FROM Reviews natural join Games WHERE uid = %s", (userid,))
        existing_reviews = list(cursor.fetchall())
        return render_template('reviews.html', existing_reviews=existing_reviews)

    elif request.method == "POST":
        gid = session['gid']

        rating = float(request.form.get('rating'))
        content = request.form.get('comment')

        # Add a review for the user and game using raw SQL query
        cursor.execute("SELECT * FROM Reviews WHERE uid = %s AND gid = %s", (userid, gid))
        existing_review = cursor.fetchall()
        if existing_review != ():
            cursor.execute("UPDATE Reviews SET rating = %s, content = %s WHERE uid = %s AND gid = %s", (rating, content, userid, gid))
            connection.commit()
            flash("Review updated successfully!", 'success')
        else:
            cursor.execute("INSERT INTO Reviews (uid, gid, rating, content) VALUES (%s, %s, %s, %s)", (userid, gid, rating, content))
            connection.commit()
            flash("Review added successfully!", 'success')

        # Fetch existing reviews for the game
        cursor.execute("SELECT * FROM Reviews WHERE gid = %s", (gid,))
        existing_reviews = cursor.fetchall()

        return redirect(url_for('games.game'))
    
@reviews_bp.route('/remove', methods=['POST'])
def remove_review():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    gid = request.form['gid']
    cursor.execute("DELETE from Reviews WHERE uid=%s and gid=%s", (userid, gid))
    
    connection.commit()
    flash(f'Successfully removed review')

    cursor.execute("SELECT gid, title, rating, content FROM Reviews natural join Games WHERE uid = %s", (userid,))
    existing_reviews = list(cursor.fetchall())
    return render_template('reviews.html', existing_reviews=existing_reviews)