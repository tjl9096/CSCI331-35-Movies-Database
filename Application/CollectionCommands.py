import UserCommands

def createCollection(curs, conn):
    currentUser = UserCommands.currentUser
    collection_name = input('Collection name: ')

    curs.execute('SELECT max(collection_id) FROM \"Collection\"')
    maxId = curs.fetchall()
    maxId = maxId[0][0]

    curs.execute(f'INSERT INTO \"Collection\"(user_id, collection_id, name) VALUES ({currentUser.user_id}, {maxId + 1}, \'{collection_name}\')')
    conn.commit()

def listCollections(curs):
    currentUser = UserCommands.currentUser
    
    curs.execute('SELECT user_id, collection_id, name FROM \"Collection\" WHERE user_id = ' + str(currentUser.user_id) + ' ORDER BY name ASC')
    result = curs.fetchall()
    
    print('Collection Name | Number of Movies | Total Length of Movies')
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
        
        print(collection_name, '|', total_collection_num, '|', str(collection_hours) + ':' + str(collection_min))
    print('-------------------------------')
