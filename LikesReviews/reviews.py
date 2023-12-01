from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for, session
from app import pool

@likesreviews.route('/reviews', methods=['GET', 'POST'])
def review_game():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    userid = session['userid']
    connection = pool.raw_connection()
    cursor = connection.cursor()

    

    if request.method == "GET":
        gamename = request.args.get['gamename']
        gameid = cursor.execute("SELECT gid FROM Games WHERE title = %s", (gamename,))

        cursor.execute("SELECT * FROM Reviews WHERE gid = %s", (gameid,))
        existing_reviews = cursor.fetchall()
        return render_template('review.html', gameid=gameid, existing_reviews=existing_reviews)

    elif request.method == "POST":
        gamename = request.form['gamename']
        gameid = cursor.execute("SELECT gid FROM Games WHERE title = %s", (gamename,))

        rating = float(request.form.get('rating'))
        content = request.form.get('content')

        # Add a review for the user and game using raw SQL query
        cursor.execute("INSERT INTO Reviews (uid, gid, rating, content) VALUES (%s, %s, %s, %s)", (userid, gameid, rating, content))
        connection.commit()
        flash("Review added successfully!", 'success')

        # Fetch existing reviews for the game
        cursor.execute("SELECT * FROM Reviews WHERE gid = %s", (gameid,))
        existing_reviews = cursor.fetchall()

        return render_template('review.html', gameid=gameid, existing_reviews=existing_reviews)