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

    print("Yay! you watched a movie. Enter the command rate_movie if you would like to rate this movie!")
    conn.commit()

def watchCollection(curs, conn):
    currentUser = UserCommands.currentUser

    if currentUser == None:
        print("Please log in to rate a movie")
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

    print("Yay! you watched a collection. Enter the command rate_movie if you would like to rate a movie!")
    conn.commit()

def top10Movies(curs):
    currentUser = UserCommands.currentUser

    if currentUser == None:
        print("Please log in to get your top 10 movie")
        return

    curs.execute(f'SELECT movie_id, title, watchcount, avgrating from (SELECT userwatches.movie_id as movie_id, title, userwatches.watchcount, userrates.avgrating from (SELECT movie_id, count(movie_id) as watchcount from "Watches" where user_id = {currentUser.user_id} group by movie_id) as userwatches left join (SELECT movie_id, avg(rating) as avgrating from "Rates" where user_id = {currentUser.user_id} group by movie_id) as userrates on userrates.movie_id = userwatches.movie_id join "Movie" on userwatches.movie_id = "Movie".movie_id) as userwatchesratings order by case when avgrating is null then 0 else avgrating end desc, watchcount desc limit 10;')

    result = curs.fetchall()

    if len(result) == 0:
        print("You must first watch and rate movies to get your top 10")
        return

    print('Movie ID | Movie Title | Watch Count | Your average rating')

    for movie_info in result:
        print(movie_info[0], "|", movie_info[1], "|", movie_info[2], "|", movie_info[3])


def forMe(curs):
    currentUser = UserCommands.currentUser

    if currentUser == None:
        print("Please log in to get recommendations")
        return

    curs.execute(f'select movie_id, title from (select movie_id, count(movie_id) as count from (select user_id from (select u.user_id, (select genre_name from "Watches" natural join "Movie_Type" natural join "Genre" where user_id = u.user_id group by genre_name order by count(genre_name) desc limit 1) as topgenre from "User" u) as uit where topgenre = (select genre_name from "Watches" natural join "Movie_Type" natural join "Genre" where user_id = {currentUser.user_id} group by genre_name order by count(genre_name) desc limit 1) limit 10) as similar_users natural join "Watches" group by movie_id order by count(movie_id) desc) rec_movies natural join "Movie" order by count desc limit 10;')

    result = curs.fetchall()

    if len(result) == 0:
        print("You must first watch and rate movies to get your top 10")
        return

    print('Movie ID | Movie Title')

    for movie_info in result:
        print(movie_info[0], "|", movie_info[1])

def top20Recommends(curs):
    currentUser = UserCommands.currentUser

    if currentUser == None:
        print("Please log in to get recommendations")
        return

    curs.execute('''select  *
                        from
                        (select userwatches.movie_id as movie_id, title, userwatches.watchcount as total, userrates.avgrating
                            from
                                (select movie_id, count(movie_id) as watchcount
                                    from "Watches"
                                    where watch_date >= CURRENT_DATE - INTERVAL '90 days'
                                    group by movie_id) as userwatches
                                left join

                                (select movie_id, avg(rating) as avgrating
                                    from "Rates"
                                    where date >= CURRENT_DATE - INTERVAL '90 days'
                                    group by movie_id) as userrates

                                on userrates.movie_id = userwatches.movie_id

                                join

                                "Movie" on userwatches.movie_id = "Movie".movie_id
                            ) as userwatchesratings
                        group by userwatchesratings.movie_id, userwatchesratings.title, userwatchesratings.avgrating, userwatchesratings.total
                        order by total desc, coalesce(avgrating) desc limit 20;
                        ''')

    result = curs.fetchall()

    print('Sr No | Movie Title')
    for i, movie_info in enumerate(result):
        print(i+1, "|", movie_info[1])

def top20FriendRecommends(curs):
    currentUser = UserCommands.currentUser

    if currentUser == None:
        print("Please log in to get recommendations.")
        return

    sql = "select m.title as title, round(r.avg_rating, 2) as avg_rating, coalesce(p.play_count, 0) as play_count \
from ( \
        ( \
            ( \
                select movie_id, avg(rating) as avg_rating \
                from \"Rates\" \
                where user_id in ( \
    select friend_id \
    from \"Friends\" \
    where user_id = %s) \
                group by movie_id \
            ) as r \
            left join ( \
                select movie_id, count(movie_id) as play_count \
                from \"Watches\" \
                where user_id in ( \
    select friend_id \
    from \"Friends\" \
    where user_id = %s) \
                group by movie_id \
            ) as p \
        on r.movie_id = p.movie_id) \
        left join ( \
            select movie_id, title \
            from \"Movie\" \
        ) as m \
        on r.movie_id = m.movie_id) \
order by avg_rating desc, play_count desc, title asc limit 20;"
    val = (currentUser.user_id, currentUser.user_id)
    curs.execute(sql, val)

    result = curs.fetchall()

    if result == []:
        print("You have no friends.")
    else:
        print('Title | Rating | Plays')
        print('-----------------------------------------')
        for movie_info in result:
            print(movie_info[0], "|", movie_info[1], "|", movie_info[2])
        print('-----------------------------------------')
    