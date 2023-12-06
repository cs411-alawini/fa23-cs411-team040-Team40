# Stored Procedure 1
## Recommendation System
This stored procedure returns a Games information table consisting of the gid, title, link, and introduction that a user's friends likes where the avg rating of the 
Friends' reviews are over 7 and is supported by more than 2 platforms.

```mysql=
DELIMITER //
Create procedure Game_recommender(user varchar(255))
Begin
	declare current_gid int;
    declare current_title varchar(255);
    declare current_link varchar(255);
    declare current_introduction varchar(255);
    declare num_platforms int;
	Declare done boolean default false;
	Declare game cursor for (select g.gid, g.title, g.link, g.introduction
				      from (select uid from Friends f where f.uid = user) as userFriends
                      join Likes l on l.uid = userFriends.uid
                      join Reviews r on r.uid = userFriends.uid
                      join Games g on g.gid = r.gid
                      group by gid, title
                      having avg(rating) >= 7);
                      
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	DROP TABLE IF EXISTS ResultTable;
    create table ResultTable(gid int, title varchar(255), link varchar(255), introduction varchar(255));
    
    open game;
		cloop: loop
        fetch game into current_gid, current_title, current_link, current_introduction;
        set num_platforms = (select count(*) 
							 from Games g 
                             natural join Supports 
                             where g.gid = current_gid
                             group by g.gid);
		if done then
			leave cloop;
		end if;
        
        if num_platforms >= 2 then
			insert into ResultTable Values(current_gid, current_title, current_link, current_introduction);
		end if;
        end loop cloop;
        
        select * from ResultTable order by title;
end;
//
Delimiter ;
```

# Stored Procedure 2
## Search System
This stored procedure returns a Games information table consisting of the gid, title, link, producerName, and Price of games that match the specified criteria in the input.

```mysql=
DELIMITER $$

CREATE PROCEDURE SearchGames (
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
END$$
DELIMITER ;
```

# Trigger 1
## LoginSignup Trigger

This trigger makes sure that no duplicate user credentials are present in the Users table. This is done by checking that the newly created username is not in the Users table before inserting it.

```mysql=
CREATE TRIGGER verifyUserSignup before insert on Users
    IF NEW.username in (select username from Users) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'An error occurred';
    END IF;
```