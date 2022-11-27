# Clint Steadman
# CSD310 Mod 7.2 Assignment
# 11/26/22
#
# connect to movies database and display queries

import mysql.connector
from mysql.connector import errorcode

# Declare variable
db = ""


# configure movies db connection. fixed from previous assignment
def connect():
    global db
    config = {
        'user': 'movies_user',
        'password': 'popcorn',
        'host': 'localhost',
        'port': '3306',
        'database': 'movies',
        'raise_on_warnings': True
    }

    try:
        db = mysql.connector.connect(**config)

        print(
            "\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                        config["database"]))

        input("\n\n Press any key to continue...")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password is invalid")

        elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)

    finally:
        db


# connect to database
connect()
cursor = db.cursor()

# extra line for output
print()

# Query 1
print("-- DISPLAYING Studio RECORDS --")
cursor.execute("SELECT studio_id, studio_name FROM movies.studio")
studio = cursor.fetchall()
for studio_id, studio_name in studio:
    print("Studio ID: {}\nStudio Name: {}\n".format(studio_id, studio_name))

# Query 2
print("-- DISPLAYING Genre RECORDS --")
cursor.execute("SELECT genre_id, genre_name FROM movies.genre")
genre = cursor.fetchall()
for genre_id, genre_name in genre:
    print("Genre ID: {}\nGenre Name: {}\n".format(genre_id, genre_name))

# Query 3
print("-- DISPLAYING Short Film RECORDS --")
cursor.execute("SELECT film_name, film_runtime FROM movies.film WHERE film_runtime < 120")
film = cursor.fetchall()
for film_name, film_runtime in film:
    print("Film Name: {}\nRuntime: {}\n".format(film_name, film_runtime))

# Query 4
print("-- DISPLAYING Director RECORDS in Order --")
cursor.execute("SELECT film_name, film_director FROM movies.film Order By film_director")
film = cursor.fetchall()
for film_name, film_director in film:
    print("Film Name: {}\nDirector: {}\n".format(film_name, film_director))
