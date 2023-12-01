from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
import csv 
from db import mysql

search = Blueprint("search", __name__)

@search.route("/search", methods=['GET'])
def get_search_term():
    if "username" not in session:
        return redirect(url_for("login.login"))
    pattern = request.args.get("search", type=str) or None
    genres = request.args.getlist("search_genres", type=int) or None
    producers = request.args.getlist("search_producers", type=int) or None
    platforms = request.args.getlist("search_platforms", type=int) or None
    lowest_price = request.args.getlist("search_lprice", type=int) or None
    highest_price = request.args.getlist("search_hprice", type=int) or None
    
    cur = mysql.connection.cursor()
    query = """
SELECT DISTINCT Games.*
FROM Games
LEFT JOIN GameType ON Games.gid = GameType.gid
LEFT JOIN Products ON Games.gid = Products.gid
LEFT JOIN Supports ON Games.gid = Supports.gid
LEFT JOIN (SELECT p.* FROM Prices p JOIN 
           (SELECT gid, MAX(Date) as LatestDate FROM Prices GROUP BY gid) as latest_prices 
           ON p.gid = latest_prices.gid AND p.Date = latest_prices.LatestDate) LatestPrices
WHERE
    (Games.title LIKE "%%s%" OR %s IS NULL) AND
    (GameType.genreID IN %s OR %s IS NULL) AND
    (Products.producerID IN %s OR %s IS NULL) AND
    (Supports.platformID IN %s OR %s IS NULL) AND
    (LatestPrices.Finalprice >= %s OR %s IS NULL) AND
    (LatestPrices.Finalprice <= %s OR %s IS NULL);
    """
    cur.execute(query, (pattern, pattern, 
                        genres, genres, 
                        producers, producers, 
                        platforms, platforms,
                        lowest_price, lowest_price,
                        highest_price, highest_price))
    games = cur.fetchall()
    return games