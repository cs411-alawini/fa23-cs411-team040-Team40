from flask import Flask, render_template, jsonify, redirect, request, url_for, flash, session, Blueprint
# from google.cloud.sql.connector import Connector
# import sqlalchemy
# import pymysql
# from db import pool

app = Flask(__name__)
app.secret_key = 'team40'



# initialize Connector object
# function to return the database connection
# def getconn() -> pymysql.connections.Connection:
#     connector = Connector()
#     conn: pymysql.connections.Connection = connector.connect(
#         "cs-411-team:us-central1:myinstance",
#         "pymysql",
#         user="root",
#         password="team40",
#         db="steam"
#     )
#     return conn


# # create connection pool
# pool = sqlalchemy.create_engine(
#     "mysql+pymysql://",
#     creator=getconn,
# )


from Friends.friends import friends_bp
from Games.games import games_bp
from Login.loginSignup import login_bp
from Likes.likes import likes_bp
from Search.search import search_bp
from Reviews.reviews import reviews_bp
from Recommends.recommends import recommends_bp

app.register_blueprint(friends_bp)
app.register_blueprint(games_bp)
app.register_blueprint(login_bp)
app.register_blueprint(search_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(recommends_bp)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)