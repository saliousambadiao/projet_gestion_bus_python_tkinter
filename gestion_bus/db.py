import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="username",
            password="password",
            database="projetexamen"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Erreur lors de la connexion à MySQL", e)
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connexion MySQL fermée")
