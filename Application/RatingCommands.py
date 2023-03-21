import UserCommands
from datetime import datetime
def rateMovie(curs, conn):
    currentUser = UserCommands.currentUser

    if currentUser == None:
        print("Please log in to rate a movie")
        return
    
    curs.execute('SELECT movie_id from \"Watches\" where user_id = ' + str(currentUser.user_id))
    movies = curs.fetchall()
    watched_movies = []
    for movie in movies:
        watched_movies.append(str(movie[0]))

    movie_to_rate = input("Please list the id of the movie you would like to rate: ")

    if movie_to_rate not in watched_movies:
        print("You can only rate movies that you have watched")
        return
    
    rating = 0

    good_ratings = ['1', '2', '3', '4', '5']
    while True:
        rating = input("What would you like to rate the movie (1-5)? ")
        if rating not in good_ratings:
            print("You can only rate a movie with an integer value between 1 and 5 (inclusive) ")
        else:
            break
    
    today = datetime.now()
    today_str = today.strftime('%Y-%m-%d')

    curs.execute(f'SELECT rating FROM \"Rates\" where user_id = ' + str(currentUser.user_id) + ' AND movie_id = ' + movie_to_rate)
    result = curs.fetchall()

    already_rated = True
    if len(result) == 0:
        already_rated = False

    if not already_rated:
        curs.execute(f'INSERT INTO \"Rates\"(user_id, movie_id, rating, date) VALUES ({currentUser.user_id}, {movie_to_rate}, {rating}, \'{today_str}\')')
    else:
        curs.execute('UPDATE \"Rates\" set rating = ' + rating + 'WHERE user_id = ' + str(currentUser.user_id) + ' AND movie_id = ' + movie_to_rate)
    conn.commit()
