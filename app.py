from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
from flask import Flask

app = Flask(__name__)


# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "cs-411-team:us-central1:myinstance",
        "pymysql",
        user="root",
        password="team40",
        db="steam"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

if __name__ == '__main__':
    app.run()