from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

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

with pool.connect() as db_conn:
    result = db_conn.execute(sqlalchemy.text("SELECT * from Users")).fetchall()

    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    # db_conn.commit()

    for row in result:
        print(row)