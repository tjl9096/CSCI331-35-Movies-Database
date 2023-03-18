from datetime import date
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

    sqlCommand = 'SELECT * FROM \"User\" WHERE username = \'' + str(user_username) + '\' and password = \'' + str(user_password) +'\''
    curs.execute(sqlCommand)
    result = curs.fetchall()

    if(len(result) != 1):
        print('username or password is incorrect')
        return
    
    user = result[0]

    currentUser = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
    currentUser.last_access_date = date.today()
    
    curs.execute(f'update \"User\" set last_access_date = \'{currentUser.last_access_date}\' where user_id = \'{currentUser.user_id}\'')
    conn.commit()

    print('log in success!')


def logout():
    global currentUser
    currentUser = None


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

    user_firstname = input('firstname: ')
    user_firstname = user_firstname.replace(' ', '')
    user_lastname = input('lastname: ')
    user_lastname = user_lastname.replace(' ', '')

    curs.execute('SELECT max(user_id) FROM \"User\"')
    maxId = curs.fetchall()
    maxId = maxId[0][0]
    currentUser = User(maxId + 1, date.today(), user_username, user_password, user_firstname, user_lastname, date.today())

    curs.execute(f'INSERT INTO \"User\"(user_id, last_access_date, username, password, first_name, last_name, creation_date) VALUES ({str(currentUser.user_id)}, \'{currentUser.last_access_date}\', \'{currentUser.username}\', \'{currentUser.password}\', \'{currentUser.first_name}\', \'{currentUser.last_name}\', \'{currentUser.creation_date}\')')
    conn.commit()


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
    print('username | firstname | lastname')
    print('-------------------------------')
    for res in result:
        print(res[1], '|', res[2], '|' , res[3])
    print('-------------------------------')


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


def listFriendedMe(curs):
    global currentUser
    if(currentUser == None):
        print('Please log in to view who friended you')
        return

    result = []
    curs.execute(f'SELECT user_id, username, first_name, last_name from "User" where user_id in (select user_id FROM "Friends" WHERE friend_id = \'{currentUser.user_id}\')')

    result = curs.fetchall()

    if(len(result) == 0):
        print('No one has friended you.')
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
    unfriend_id = input('friend id to unfriend: ')
    curs.execute(f'insert into "Friends" (user_id, friend_id) values (\'{currentUser.user_id}\', \'{unfriend_id}\')')
    conn.commit()


def removeFriend(curs, conn):
    global currentUser
    if(currentUser == None):
        print('Please log in to unfriend someone')
        return
    unfriend_id = input('friend id to unfriend: ')
    curs.execute(f'delete from "Friends" WHERE user_id = \'{currentUser.user_id}\' and friend_id = \'{unfriend_id}\'')
    conn.commit()

