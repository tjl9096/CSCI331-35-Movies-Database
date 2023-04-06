from datetime import date
import hashlib

class User:
    def __init__(self, user_id, last_access_date, username, password, first_name, last_name, creation_date):
        self.user_id = user_id
        self.last_access_date = last_access_date
        self.username = username 
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.creation_date = creation_date


currentUser: User = None 


def getUser(curs):
    user_id = input('user_id: ')
    sqlCommand = 'SELECT * FROM \"User\" WHERE user_id = ' + str(user_id)
    curs.execute(sqlCommand)
    result = curs.fetchall()
    print(result)


def login(curs, conn):
    global currentUser
    user_username = input('username: ')
    user_password = input('password: ')
    user_password = user_password.encode()
    hash_user_password = hashlib.sha256(user_password)

    sqlCommand = 'SELECT * FROM \"User\" WHERE username = \'' + str(user_username) + '\' and password = \'' + str(hash_user_password.hexdigest()) +'\''
    curs.execute(sqlCommand)
    result = curs.fetchall()

    if(len(result) != 1):
        print('username or password is incorrect')
        return
    
    user = result[0]

    currentUser = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
    currentUser.last_access_date = date.today()
    
    curs.execute(f'update \"User\" set last_access_date = current_date where user_id = \'{currentUser.user_id}\'')
    conn.commit()

    print('log in success!')


def logout():
    global currentUser
    currentUser = None
    print('log out success!')


def createAccount(curs, conn):
    global currentUser
    # select a username
    while(True):
        user_username = input('username: ')
        user_username = user_username.replace(' ', '')
        curs.execute('SELECT * FROM \"User\" WHERE username = \'' + str(user_username) + '\'')
        result = curs.fetchall()
        if len(result) == 0:
            break 
        else: 
            print('That username is already taken.')

    # select a password
    while(True):
        user_password = input('password: ')
        user_password = user_password.replace(' ', '')
        retype_user_password = input('retype password: ')
        retype_user_password = retype_user_password.replace(' ', '')

        if(user_password == retype_user_password):
            break; 
        else:
            print('passwords did not match, try again.')

    hash_user_password = user_password.encode()
    hash_user_password = hashlib.sha256(hash_user_password)

    user_firstname = input('firstname: ')
    user_firstname = user_firstname.replace(' ', '')
    user_lastname = input('lastname: ')
    user_lastname = user_lastname.replace(' ', '')

    curs.execute('SELECT max(user_id) FROM \"User\"')
    maxId = curs.fetchall()
    maxId = maxId[0][0]
    currentUser = User(maxId + 1, date.today(), user_username, hash_user_password.hexdigest(), user_firstname, user_lastname, date.today())

    curs.execute(f'INSERT INTO \"User\"(user_id, last_access_date, username, password, first_name, last_name, creation_date) VALUES ((SELECT max(user_id) FROM \"User\")+1, current_date, \'{currentUser.username}\', \'{currentUser.password}\', \'{currentUser.first_name}\', \'{currentUser.last_name}\', current_date)')
    conn.commit()
    print('create account success!')


def searchFriends(curs):
    result = []

    while len(result) == 0:
        email_search = input('search by email: ')

        curs.execute(f'SELECT user_id, username, first_name, last_name from "User" where user_id in (SELECT user_id FROM "Email" WHERE email like \'%{email_search}%\')')
        result = curs.fetchall()

        if(len(result) == 0):
            print('no users with that email found')
        else:
            break
    print('user_id | username | firstname | lastname')
    print('-----------------------------------------')
    for res in result:
        print(res[0], '|', res[1], '|', res[2], '|' , res[3])
    print('-----------------------------------------')


def listTotalFriends(curs):
    global currentUser
    if(currentUser == None):
        print('Please log in to view your friends')
        return

    curs.execute(f'SELECT count(*) from "Friends" WHERE user_id = {currentUser.user_id}')

    result = curs.fetchall()

    print("You have friended " + str(result[0][0]) + " people")


def listFriends(curs):
    global currentUser
    if(currentUser == None):
        print('Please log in to view your friends')
        return

    result = []
    curs.execute(f'SELECT user_id, username, first_name, last_name from "User" where user_id in (select friend_id FROM "Friends" WHERE user_id = \'{currentUser.user_id}\')')

    result = curs.fetchall()

    if(len(result) == 0):
        print('You have no friends.')
        return
    
    print('People who you have friended')
    print('user_id | username | firstname | lastname')
    print('-----------------------------------------')
    for res in result:
        print(res[0], '|', res[1], '|', res[2], '|' , res[3])
    print('-----------------------------------------')


def listTotalFriendedMe(curs):
    global currentUser
    if(currentUser == None):
        print('Please log in to view your friends')
        return

    curs.execute(f'SELECT count(*) from "Friends" WHERE friend_id = {currentUser.user_id}')

    result = curs.fetchall()

    print(str(result[0][0]) + " people have friended you")


def listFriendedMe(curs):
    global currentUser
    if(currentUser == None):
        print('Please log in to view who friended you')
        return

    result = []
    curs.execute(f'SELECT user_id, username, first_name, last_name from "User" where user_id in (select user_id FROM "Friends" WHERE friend_id = \'{currentUser.user_id}\')')

    result = curs.fetchall()

    if(len(result) == 0):
        print('No one has friended you')
        return
    
    print('People who have friended you')
    print('user_id | username | firstname | lastname')
    print('-----------------------------------------')
    for res in result:
        print(res[0], '|', res[1], '|', res[2], '|' , res[3])
    print('-----------------------------------------')


def addFriend(curs, conn):
    global currentUser
    if(currentUser == None):
        print('Please log in to friend someone')
        return
    friend_id = input('friend id to friend: ')
    curs.execute(f'insert into "Friends" (user_id, friend_id) values (\'{currentUser.user_id}\', \'{friend_id}\')')
    conn.commit()
    print('friend added!')


def removeFriend(curs, conn):
    global currentUser
    if(currentUser == None):
        print('Please log in to unfriend someone')
        return
    unfriend_id = input('friend id to unfriend: ')
    curs.execute(f'delete from "Friends" WHERE user_id = \'{currentUser.user_id}\' and friend_id = \'{unfriend_id}\'')
    conn.commit()
    print('friend removed!')

def searchMovie(curs):
    global currentUser
    if(currentUser == None):
        print('Please log in to search for movies')
        return
      
    search_by = input('Search a movie by name, release date, cast members, studio, or genre: \n')
    queryBy = '' 

    match search_by:
        case 'name':
            queryBy = 'title'
        case 'release date':
            queryBy = 'release_date'
        case 'cast members':
            queryBy = 'Actors.name'
        case 'studio':
            queryBy = 'Base.platform_name'
        case 'genre':
            queryBy = 'Base.genre_name'
        case _:
            print('Please select one of the above options')
            return

    search_field = input ('Enter the search term: \n')
    
    result = [] 

    if search_by == 'release date':
        curs.execute(f'''SELECT title as Title, Actors.name as Actors, Directors.name as Directors, genre_name as Genre, Base.length "Length ", mpaa_rating, ROUND(AVG(rating),2)
                            FROM ("Movie"
                                natural join "Hosts_On"
                                natural join "Movie_Type"
                                natural join "Genre"
                                natural join "Release_Platform"
                                )
                                as BASE
                            left outer join "Rates" on BASE.movie_id = "Rates".movie_id
                            left outer join "Directs" on BASE.movie_id = "Directs".movie_id
                            left outer join "Acts" on BASE.movie_id = "Acts".movie_id
                            left outer join "Contributor" Actors on "Acts".contributor_id = Actors.contributor_id
                            left outer join "Contributor" Directors on "Directs".contributor_id = Directors.contributor_id
                            where {queryBy} = \'{search_field}\'
                            group by title, Actors.name,Directors.name, genre_name, release_date, Base.length, mpaa_rating
                            order by title ASC, release_date DESC;''')         
    else:
        curs.execute(f'''SELECT title as Title, Actors.name as "Actors", Directors.name as "Directors", genre_name as "Genre", Base.length "Length ", mpaa_rating, ROUND(AVG(rating),2)
                            FROM ("Movie"
                                natural join "Hosts_On"
                                natural join "Movie_Type"
                                natural join "Genre"
                                natural join "Release_Platform"
                                )
                                as BASE
                            left outer join "Rates" on BASE.movie_id = "Rates".movie_id
                            left outer join "Directs" on BASE.movie_id = "Directs".movie_id
                            left outer join "Acts" on BASE.movie_id = "Acts".movie_id
                            left outer join "Contributor" Actors on "Acts".contributor_id = Actors.contributor_id
                            left outer join "Contributor" Directors on "Directs".contributor_id = Directors.contributor_id
                            where LOWER({queryBy}) like LOWER(\'%{search_field}%\')
                            group by title, Actors.name,Directors.name, genre_name, release_date, Base.length, mpaa_rating
                            order by title ASC, release_date DESC;''')
    
    result = curs.fetchall()
    displayResults(result)

    sort = input('Would you like to sort the results? (y/n): ')
    if sort == 'y':
        sortField = input('Sort by name, release year, genre or studio \n')
        sortOrder = input('Sort ascending or descending? (a/d) \n')
            
        if sortOrder == 'd':
            sortOrder = 'DESC'
        else:
            sortOrder = 'ASC'
        
        if sortField == 'name':
            sortField = 'title'
        elif sortField == 'release year':
            sortField = 'release_date'
        elif sortField == 'genre':
            sortField = 'BASE.genre_name'
        elif sortField == 'studio':
            sortField = 'Base.platform_name'
        else:
            sortField = 'title'
            
        if search_by == 'release date':
            curs.execute(f'''SELECT title as Title, Actors.name as Actors, Directors.name as Directors, genre_name as Genre, Base.length "Length ", mpaa_rating, ROUND(AVG(rating),2)
                                FROM ("Movie"
                                    natural join "Hosts_On"
                                    natural join "Movie_Type"
                                    natural join "Genre"
                                    natural join "Release_Platform"
                                    )
                                    as BASE
                                left outer join "Rates" on BASE.movie_id = "Rates".movie_id
                                left outer join "Directs" on BASE.movie_id = "Directs".movie_id
                                left outer join "Acts" on BASE.movie_id = "Acts".movie_id
                                left outer join "Contributor" Actors on "Acts".contributor_id = Actors.contributor_id
                                left outer join "Contributor" Directors on "Directs".contributor_id = Directors.contributor_id
                                where {queryBy} = \'{search_field}\'
                                group by title, Actors.name,Directors.name, genre_name, release_date, Base.length, mpaa_rating
                                order by {sortField} {sortOrder}''')         
        else:
            curs.execute(f'''SELECT title as Title, Actors.name as "Actors", Directors.name as "Directors", genre_name as "Genre", Base.length "Length ", mpaa_rating, ROUND(AVG(rating),2)
                                FROM ("Movie"
                                    natural join "Hosts_On"
                                    natural join "Movie_Type"
                                    natural join "Genre"
                                    natural join "Release_Platform"
                                    )
                                    as BASE
                                left outer join "Rates" on BASE.movie_id = "Rates".movie_id
                                left outer join "Directs" on BASE.movie_id = "Directs".movie_id
                                left outer join "Acts" on BASE.movie_id = "Acts".movie_id
                                left outer join "Contributor" Actors on "Acts".contributor_id = Actors.contributor_id
                                left outer join "Contributor" Directors on "Directs".contributor_id = Directors.contributor_id
                                where LOWER({queryBy}) like LOWER(\'%{search_field}%\')
                                group by title, Actors.name,Directors.name, genre_name, release_date, Base.length, mpaa_rating, Base.platform_name
                                order by {sortField} {sortOrder};''')
        
        result = curs.fetchall()
        displayResults(result)


def displayResults(result):
    print('Title | Actors | Directors | Genre | Length | MPAA Rating | Average Rating')
    print('-------------------------------------------------------------------------')
    for res in result:
        print(res[0], '|', res[1], '|', res[2], '|' , res[3], '|', res[4], '|', res[5], '|', res[6])
    print('-------------------------------------------------------------------------')
    