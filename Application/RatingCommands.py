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

# if the top 5 new release of the month seems like it isn't working, 
# just change the current year and month to the hard coded values to see it does 
def top_five_month(curs):
    currentUser = UserCommands.currentUser

    if currentUser == None:
        print("Please log in to see top 5 new releases of the month")
        return

    today = datetime.today()
    curr_year = today.strftime("%Y")    # change to "2023"
    curr_month = today.strftime("%m")   # change to "03"

    curs.execute(f'select * from (select * from "Movie" where date_part(\'month\', release_date) = {curr_month} and date_part(\'year\', release_date) = {curr_year}) as currMonth inner join (SELECT movie_id, title, watchcount, avgrating from (SELECT userwatches.movie_id as movie_id, title, userwatches.watchcount, userrates.avgrating from (SELECT movie_id, count(movie_id) as watchcount from "Watches" group by movie_id) as userwatches left join (SELECT movie_id, avg(rating) as avgrating from "Rates" group by movie_id) as userrates on userrates.movie_id = userwatches.movie_id join "Movie" on userwatches.movie_id = "Movie".movie_id) as userwatchesratings order by case when avgrating is null then 0 else avgrating end desc, watchcount desc) as topMovies on currMonth.movie_id = topMovies.movie_id order by case when avgrating is null then 0 else avgrating end desc, watchcount desc limit 5')

    result = curs.fetchall()

    if len(result) == 0:
        print("There is not yet any top 5 new releases for the current month :(")
        return

    print('Movie ID | Movie Title')

    for movie_info in result:
        print(movie_info[0], "|", movie_info[1])
