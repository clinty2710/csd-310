# Clint Steadman
# CSD310 Mod 8.2 Assignment
# 11/28/22
#
# connect to movies database and update/delete entries

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


# Establish connection
connect()
cursor = db.cursor()


def show_films(cursor, title):
    # Method to execute an inner join on all tables,
    # iterate over the dataset and output the results to the terminal window.

    # Inner join query
    cursor.execute(
        "SELECT film_name as Name, film_director as Director, genre_name as Genre,\
        studio_name as 'Studio Name' FROM film INNER JOIN genre ON \
        film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id")

    # Get the results from the cursor object
    films = cursor.fetchall()

    print("\n -- {} --".format(title))

    # Iterate over the film data set and display the results
    for film in films:
        print(
            "Film Name: {}\nDirector: {}\nGenre Name: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))


show_films(cursor, "DISPLAYING FILMS")

cursor.execute(
    "INSERT INTO Film (film_id, film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) \
    VALUES (4, 'Lincoln', 2012, 150, 'Steven Spielberg', 1, 3) ")

show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

cursor.execute("UPDATE film SET genre_id = 1 WHERE film_name = 'Alien'")

show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator'")

show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

# commit changes in database
db.commit()


