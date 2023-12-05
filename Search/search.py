from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
import csv 
from db import pool

search_bp = Blueprint("search", __name__, url_prefix="/gamesearch")

@search_bp.route('/', methods=['GET'])
def get_search_term():
    return render_template("search.html")

@search_bp.route("/results", methods=['GET'])
def get_search_results():
    pattern = request.args.get("pattern", type=str) or None
    genres = request.args.getlist("genres", type=int) or None
    producer = request.args.get("producer", type=str) or None
    platforms = request.args.getlist("platforms", type=int) or None
    lowest_price = request.args.get("lprice", type=int) or None
    highest_price = request.args.get("hprice", type=int) or None
    
    connection = pool.raw_connection()
    cursor = connection.cursor()
    conditions = ["TRUE"]
    if pattern:
        conditions.append(f"Games.title LIKE '%{pattern}%'")
    if genres:
        genres = [str(i) for i in genres]
        conditions.append(f"GameType.genreID IN ({', '.join(genres)})")
    if producer:
        conditions.append(f"Producers.producerName LIKE '%{producer}%'")
    if platforms:
        platforms = [str(i) for i in platforms]
        conditions.append(f"Supports.platformID IN ({', '.join(platforms)})")
    if lowest_price:
        conditions.append(f"LatestPrices.Finalprice >= {lowest_price}")
    if highest_price:
        conditions.append(f"LatestPrices.Finalprice <= {highest_price}")
    
    query = f"""
SELECT DISTINCT Games.*
FROM Games
LEFT JOIN GameType ON Games.gid = GameType.gid
LEFT JOIN Products ON Games.gid = Products.gid
LEFT JOIN Producers ON Products.producerID = Producers.producerID
LEFT JOIN Supports ON Games.gid = Supports.gid
LEFT JOIN (SELECT p.* FROM Prices p JOIN (SELECT gid, MAX(Date) as LatestDate FROM Prices GROUP BY gid) as latest_prices 
          ON p.gid = latest_prices.gid AND p.Date = latest_prices.LatestDate) LatestPrices  ON Games.gid = LatestPrices.gid
WHERE {' AND '.join(conditions)};
    """
    #print(query)
    
    cursor.execute(query)
    games_list = cursor.fetchall()
    
    return render_template("games.html", games_list=games_list)