from flask import Flask, render_template, jsonify, redirect, request, url_for, flash, session
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql


# initialize Connector object
# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    connector = Connector()
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