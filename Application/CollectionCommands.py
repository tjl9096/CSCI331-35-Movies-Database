import UserCommands

def createCollection(curs, conn):
    currentUser = UserCommands.currentUser

    if (currentUser == None):
        print("Please log in to create a collection")
        return
    
    collection_name = input('Collection name: ')

    curs.execute('SELECT max(collection_id) FROM \"Collection\"')
    maxId = curs.fetchall()
    maxId = maxId[0][0]

    curs.execute(f'INSERT INTO \"Collection\"(user_id, collection_id, name) VALUES ({currentUser.user_id}, {maxId + 1}, \'{collection_name}\')')
    conn.commit()

def listCollections(curs):
    currentUser = UserCommands.currentUser

    if (currentUser == None):
        print("Please log in to list your collections")
        return
    
    curs.execute('SELECT user_id, collection_id, name FROM \"Collection\" WHERE user_id = ' + str(currentUser.user_id) + ' ORDER BY name ASC')
    result = curs.fetchall()
    
    print('Collection Name | Collection ID | Number of Movies | Total Length of Movies')
    print('-------------------------------')
    for collection_num in range(0, len(result)):
        collection = result[collection_num]
        collection_id = collection[1]
        collection_name = collection[2]

        curs.execute(f'SELECT movie_id FROM \"Collection_Contains\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id))
        collection_movies = curs.fetchall()

        total_collection_length = 0
        total_collection_num = 0
        for movie in collection_movies:
            curs.execute(f'SELECT length FROM \"Movie\" Where movie_id = ' + str(movie[0]))
            temp = curs.fetchall()
            total_collection_length = total_collection_length + temp[0][0]
            total_collection_num = total_collection_num + 1
        
        collection_hours = total_collection_length//60
        collection_min = total_collection_length%60
        if collection_min < 10:
            collection_min = '0' + str(collection_min)
        
        print(collection_name, '|', collection_id, '|', total_collection_num, '|', str(collection_hours) + ':' + str(collection_min))
    print('-------------------------------')

def renameCollection(curs, conn):
    currentUser = UserCommands.currentUser

    if (currentUser == None):
            print("Please log in to modify your collections")
            return

    collection_id = input('Enter the id of the collection you want to rename: ')

    curs.execute(f'SELECT name from \"Collection\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id))
    result = curs.fetchall()

    if len(result) == 0:
        print("You do not have a collection with that ID")
        print("Use \'list_collections\' to see collections you own")
        return
    
    new_name = input('What would you like to change the name to?: ')
    if len(new_name) > 50:
        new_name = new_name[0:49]
        print('Name was too long, reduced to 50 characters')

    curs.execute('UPDATE \"Collection\" set name = \''  + new_name + '\' WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id))
    conn.commit()

def deleteCollection(curs, conn):
    currentUser = UserCommands.currentUser

    if (currentUser == None):
            print("Please log in to modify your collections")
            return

    collection_id = input('Enter the id of the collection you want to delete: ')

    curs.execute(f'SELECT name from \"Collection\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id))
    result = curs.fetchall()

    if len(result) == 0:
        print("You do not have a collection with that ID")
        print("Use \'list_collections\' to see collections you own")
        return
    
    curs.execute('DELETE FROM \"Collection_Contains\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id))
    conn.commit()
    curs.execute('DELETE FROM \"Collection\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id))
    conn.commit()


def listTotalCollections(curs):
    currentUser = UserCommands.currentUser

    if (currentUser == None):
            print("Please log in to view a collection")
            return
    
    curs.execute(f'SELECT count(*) from \"Collection\" WHERE user_id = ' + str(currentUser.user_id))
    result = curs.fetchall()

    print("You have " + str(result[0][0]) + " collections"); 
    

def viewCollection(curs):
    currentUser = UserCommands.currentUser

    if (currentUser == None):
            print("Please log in to view a collection")
            return

    collection_id = input('Enter the id of the collection you want to view: ')

    curs.execute(f'SELECT name from \"Collection\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id))
    result = curs.fetchall()

    if len(result) == 0:
        print("You do not have a collection with that ID")
        print("Use \'list_collections\' to see collections you own")
        return
    
    curs.execute(f'SELECT movie_id, title, length, mpaa_rating from \"Movie\" WHERE movie_id in (SELECT movie_id from \"Collection_Contains\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id) + ')')
    result = curs.fetchall()

    if len(result) == 0:
        print("This collection is empty")
        return

    print('Movie ID | Movie Title | Length(in minutes) | MPAA Rating')

    for movie_info in result:
        print(movie_info[0], "|", movie_info[1], "|", movie_info[2], "|", movie_info[3])

def addMovieToCollection(curs, conn):
    currentUser = UserCommands.currentUser

    if (currentUser == None):
                print("Please log in to modify your collections")
                return

    collection_id = input('Enter the id of the collection you want to add a movie to: ')

    curs.execute(f'SELECT name from \"Collection\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id))
    result = curs.fetchall()

    if len(result) == 0:
        print("You do not have a collection with that ID")
        print("Use \'list_collections\' to see collections you own")
        return
    
    movie_id = input('Enter the id of the movie you want to add: ')

    curs.execute('SELECT movie_id from \"Movie\" WHERE movie_id = ' + str(movie_id))
    result = curs.fetchall()
    if len(result) == 0:
        print("A movie with this ID does not exist")
        return
    
    curs.execute('SELECT movie_id from \"Collection_Contains\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id) + ' AND movie_id = ' + str(movie_id))
    result = curs.fetchall()
    if len(result) != 0:
        print("That movie is already in your collection")
        return

    curs.execute(f'INSERT INTO \"Collection_Contains\"(user_id, collection_id, movie_id) VALUES ({str(currentUser.user_id)}, {collection_id}, {movie_id})')
    conn.commit()

def removeMovieFromCollection(curs, conn):
    currentUser = UserCommands.currentUser

    if (currentUser == None):
            print("Please log in to modify your collections")
            return

    collection_id = input('Enter the id of the collection you want to remove a movie from: ')

    curs.execute(f'SELECT name from \"Collection\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id))
    result = curs.fetchall()

    if len(result) == 0:
        print("You do not have a collection with that ID")
        print("Use \'list_collections\' to see collections you own")
        return
    
    movie_id = input('Enter the id of the movie you want to remove: ')

    curs.execute('SELECT movie_id from \"Collection_Contains\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id) + ' AND movie_id = ' + str(movie_id))
    result = curs.fetchall()
    if len(result) == 0:
        print("That movie is not in your collection")
        return
    
    curs.execute(f'DELETE from \"Collection_Contains\" WHERE user_id = ' + str(currentUser.user_id) + ' AND collection_id = ' + str(collection_id) + ' AND movie_id = ' + str(movie_id))
    conn.commit()