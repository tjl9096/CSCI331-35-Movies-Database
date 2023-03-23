import UserCommands
from datetime import datetime

def watchMovie(curs, conn):
    currentUser = UserCommands.currentUser

    if currentUser == None:
        print("Please log in to rate a movie")
        return
    
    curs.execute('SELECT movie_id from \"Movie\"')
    movie_ids = curs.fetchall()
    movies = []
    for movie in movie_ids:
        movies.append(str(movie[0]))

    movie_to_watch = input("Please list the id of the movie you would like to watch: ")

    if movie_to_watch not in movies:
        print("You can only watch movies that are present in imDBMS")
        return
    
    today = datetime.now()
    today_str = today.strftime('%Y-%m-%d %H:%M:%S')

    curs.execute(f'INSERT INTO \"Watches\"(watch_date, user_id, movie_id) VALUES (\'{today_str}\', {currentUser.user_id}, {movie_to_watch})')

    conn.commit()

def watchCollection(curs, conn):
    currentUser = UserCommands.currentUser

    if currentUser == None:
        print("Please log in to rate a move")
        return

    collection_to_watch = input("Please list the id of the collection you would like to watch: ")
    
    curs.execute(f'SELECT collection_id FROM \"Collection\" where user_id = ' + str(currentUser.user_id))
    users_collection_ids = curs.fetchall()
    users_collection = []
    for collection_id in users_collection_ids:
        users_collection.append(str(collection_id[0]))

    if collection_to_watch not in users_collection:
        print("You can only watch collections that you have created")
        return
    
    curs.execute(f'SELECT movie_id FROM \"Collection_Contains\" where user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + collection_to_watch)
    movie_ids = curs.fetchall()
    movies_to_watch = []
    for movie in movie_ids:
        movies_to_watch.append(str(movie[0]))

    today = datetime.now()
    today_str = today.strftime('%Y-%m-%d %H:%M:%S')
    
    for movie_to_watch in movies_to_watch:
        curs.execute(f'INSERT INTO \"Watches\"(watch_date, user_id, movie_id) VALUES (\'{today_str}\', {currentUser.user_id}, {movie_to_watch})')

    conn.commit()
