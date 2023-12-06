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
    #genres = request.args.getlist("genres") or None
    genres = ','.join(request.args.getlist("genres")) or None
    producer = request.args.get("producer", type=str) or None
    #platforms = request.args.getlist("platforms") or None
    platforms = ','.join(request.args.getlist("platforms")) or None
    lowest_price = request.args.get("lprice", type=int) or None
    highest_price = request.args.get("hprice", type=int) or None
    
    connection = pool.raw_connection()
    cursor = connection.cursor()
    cursor.callproc("SearchGames", [pattern, genres, producer, platforms, lowest_price, highest_price])
    '''
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
SELECT DISTINCT Games.gid, Games.title, Games.link, Games.introduction
FROM Games
LEFT JOIN GameType ON Games.gid = GameType.gid
LEFT JOIN Products ON Games.gid = Products.gid
LEFT JOIN Producers ON Products.producerID = Producers.producerID
LEFT JOIN Supports ON Games.gid = Supports.gid
LEFT JOIN (SELECT p.* FROM Prices p JOIN (SELECT gid, MAX(Date) as LatestDate FROM Prices GROUP BY gid) as latest_prices 
          ON p.gid = latest_prices.gid AND p.Date = latest_prices.LatestDate) LatestPrices  ON Games.gid = LatestPrices.gid
WHERE {' AND '.join(conditions)};
    """
    
    cursor.execute(query)'''
    games_list = cursor.fetchall()
    #print(games_list)
    
    return render_template("games.html", games_list=games_list)



"""
CREATE DEFINER=`root`@`%` PROCEDURE `SearchGames`(
    IN in_pattern VARCHAR(255),
    IN in_genres TEXT,
    IN in_producer VARCHAR(255),
    IN in_platforms TEXT,
    IN in_lowest_price INT,
    IN in_highest_price INT
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE game_id, genre_id, platform_id INT;
    DECLARE final_price DECIMAL(10,2);
    DECLARE game_title, game_link, producer_name VARCHAR(255);
    DECLARE cur CURSOR FOR 
        SELECT g.gid, g.title, g.link, p.producerName, MAX(pr.Finalprice)
        FROM Games g
        JOIN Products pd ON g.gid = pd.gid
        JOIN Producers p ON pd.producerID = p.producerID
        JOIN Prices pr ON g.gid = pr.gid
        WHERE (in_pattern IS NULL OR g.title LIKE CONCAT('%', in_pattern, '%'))
          AND (in_producer IS NULL OR p.producerName LIKE CONCAT('%', in_producer, '%'))
          AND (in_lowest_price IS NULL OR pr.Finalprice >= in_lowest_price)
          AND (in_highest_price IS NULL OR pr.Finalprice <= in_highest_price)
        GROUP BY g.gid, g.title, g.link, p.producerName;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Temporary table to store results
    CREATE TEMPORARY TABLE IF NOT EXISTS TempSearchResults (
        GameID INT,
        Title VARCHAR(255),
        Link VARCHAR(255),
        ProducerName VARCHAR(255),
        Price DECIMAL(10,2)
    );

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO game_id, game_title, game_link, producer_name, final_price;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Check for genres and platforms if provided
        IF in_genres IS NOT NULL THEN
            SELECT DISTINCT gid INTO genre_id FROM GameType WHERE FIND_IN_SET(genreID, in_genres) AND gid = game_id;
            IF genre_id IS NULL THEN
                ITERATE read_loop;
            END IF;
        END IF;

        IF in_platforms IS NOT NULL THEN
            SELECT DISTINCT gid INTO platform_id FROM Supports WHERE FIND_IN_SET(platformID, in_platforms) AND gid = game_id;
            IF platform_id IS NULL THEN
                ITERATE read_loop;
            END IF;
        END IF;

        -- Insert into temporary table
        INSERT INTO TempSearchResults (GameID, Title, Link, ProducerName, Price) VALUES (game_id, game_title, game_link, producer_name, final_price);
    END LOOP;

    CLOSE cur;

    -- Return the results
    SELECT GameID, Title, Link FROM TempSearchResults;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS TempSearchResults;
END
"""
