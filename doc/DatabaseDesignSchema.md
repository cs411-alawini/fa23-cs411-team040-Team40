# Database Design

## ER Diagram

![ER](./image/PT1%20Stage2%20ERD.png)

## Relational Schema

```mysql
Users(
    uid: INT [PK]
    username: VARCHAR(20)
    password: VARCHAR(50)
);
```
```mysql
Games(
    gid: INT [PK]
    title: VARCHAR(255)
    introduction: VARCHAR(255)
    link: VARCHAR(255)
);
```
```mysql
Reviews(
    uid: INT [PK] [FK to Users.uid]
    gid: INT [PK] [FK to Game.gid]
    rating: Decimal
    content: VARCHAR(255)
);
```
```mysql
Platforms(
    platformID: INT [PK]
    platformName: VARCHAR(255)
);
```
```mysql
Genres(
    genreID: INT [PK]
    type: VARCHAR(30)
);
```
```mysql
Prices(
    gid: INT [PK] [FK to Game.gid]
    date: DATE [PK]
    price: Decimal
);
```
```mysql
Producers( 
    producerId: INT [PK]
    producerName: VARCHAR(50)
);
```

```mysql
Friends(
    uid: INT [PK] [FK to Users.uid]
    friendId: INT [PK] [FK to Users.uid]
);
```

```mysql
Likes(
    uid: INT [PK] [FK to Users.uid]
    gid: INT [PK] [FK to Games.gid]
);
```

```mysql
GameType(
    gid: INT [PK] [FK to Game.gid]
    genreId: INT [PK] [FK to Genres.genreID]
);
```

```mysql
Products(
    gid: INT [PK] [FK to Games.gid]
    producerId: INT [FK to Producer.producerId]
);
```

```mysql
Support(	
    gid:INT [PK] [FK to Games.gid]
    platformId: INT [PK] [FK to Platforms.platformId]
);
```

## Description & Assumption
### Entity Tables
**Users:**

Description - The **Users** table stores all user account information, including username and password. The $uid$ is the primary key. 

Assumptions - Each user has a unique uid which is associated with a unique username and all registered users should be recorded in this table.

**Games:**

Description - The **Games** table stores all game information, including title and introduction texts and URL. The $gid$ is the primary key.

Assumptions - Each game has a unique $gid$ and all games should be stored in this table.

**Genres:**

Description - The **Genres** table stores information about different genres, including the $genreId$ and the name of the genre. The $genreId$ is the primary key.

Assumptions - Each genre has a unique $genreId$ and all games’ genres should be stored in this table.

**Platforms:**

Description - The **Platforms** table stores information about different platforms, including the platform ID and the name of the platform. The $platformId$ is the primary key.

Assumptions - Each platform has a unique $platformId$ and all platforms should be stored in this table.

**Producer:**

Description - The **Producer** table stores information about the producers, including the $producerId$ and $producerName$. The $producerId$ is the primary key.

Assumptions - Each producer has a unique $producerId$ and a unique $producerName$.

**Prices (weak):**

Description - The **Prices** table stores the statistical information for the price history of the games, including the $gid$, $date$ and $price$. The $gid$ and $date$ is the primary key. 

Assumptions - The relationship between **Prices** and **Games** is one-to-many. Each game should have at least one price.

**Reviews (weak):**

Description - The **Reviews** table stores all the reviews written by users for games.

Assumptions - The relationship between **Reviews** and **Users** and that between **Reviews** and **Games** are both one-to-many. Each review can only be written by one user and be for one game. Each user can write zero or more reviews and each review is written by one user. Each game can have zero or more reviews and each review is for one game.

### Relationship Tables

**Friends:**

Description - The **Friends** table stores all friendships between two users. Both $uid$ and $friendId$ in **Friends** are referencing uid in **Users**, and they are the primary key.

Assumptions - The relationship is many-to-many. Each user can have zero or more friends. Each user can be the friend of zero or more users.

**Likes:**

Description - The **Likes** table stores the favorite games of the users. $Uid$ and $gid$ are the primary key. $Uid$ references $uid$ in Users. $Gid$ references to the $gid$ in Games.

Assumptions - The relationship is many-to-many. Each user can have zero or many favorite games. Each game can be liked by zero or many users.

**Supports:**

Description - The **Supports** table stores the information about what platforms each game supports. 

Assumptions - The relationship is many-to-many. A game can be played on one or more platforms and each platform is supported by zero or more games.

**GameType:**

Description - The **GameType** table stores the information about the genres of each game in the Games entity.

Assumptions - The relationship is many-to-many. Each game can have one or multiple genres and each genre can be associated with zero or multiple games.

**Product:**

Description - The **Product** table stores the relationship between a game and its producer, including the $gid$ and $producerId$. The $gid$ is the primary key and a foreign key referencing the $gid$ in the Game table. The $producerId$ is a foreign key referencing the $producerId$ in the Producer table.

Assumptions - The relationship is one-to-many. Each game should be produced by only one producer. A producer can produce zero or many games.


## Normalization

### Apply 3NF

**Users:** uid $\to$ username, password $^{(1)}$ ; username $\to$ uid $^{(2)}$

**Games:** gid $\to$ title, introduction, link $^{(1)}$ ; link $\to$ gid $^{(2)}$ ; title $\to$ gid $^{(2)}$

**Reviews:** uid, gid $\to$ rating, content $^{(1)}$

**Platforms:** platformId $\to$ platformName $^{(1)}$ ; platformName $\to$ platformId $^{(2)}$

**Genres:** genreId $\to$ type $^{(1)}$ ; type $\to$ genreId $^{(2)}$

**Prices:** gid, date $\to$ price $^{(1)}$

**Producer:** producerId $\to$ producerName $^{(1)}$ ; producerName $\to$ genreId $^{(2)}$

**Friends:** No non-trival FDs

**Likes:** No non-trival FDs

**GameType:** No non-trival FDs

**Product:** No non-trival FDs

**Support:** No non-trival FDs

We can see that all of our tables are in 3NF since all the LHS of every non-trivial FD is the primary key (indicated with ${(1)}$) or the RHS is part of at least one primary key (indicated with ${(2)}$).

3NF normalization was chosen because unlike BCNF, 3NF preserves functional dependencies. In addition, 3NF normalization avoids information loss. Becuase 3NF preserves functional dependencies, we do not have to create more tables to reinforce those functional dependencies. Such tables would make it so more joins would be required which is extremely computationally expensive. 
