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


def getUserUsage():
    print('Usage: getuser [user_id] ')


def getUser(curs, args):
    if len(args) != 1:
        getUserUsage()
        return
    
    user_id = args[0]
    sqlCommand = 'SELECT * FROM \"User\" WHERE user_id = ' + str(user_id)
    curs.execute(sqlCommand)
    result = curs.fetchall()
    print(result)


def loginUsage():
    print('Usage: login [username] [password]')


def login(curs, args):
    if len(args) != 2:
        loginUsage()
    
    user_username = args[0]
    user_password = args[1]

    sqlCommand = 'SELECT * FROM \"User\" WHERE username = \'' + str(user_username) + '\' and password = \'' + str(user_password) +'\''
    curs.execute(sqlCommand)
    result = curs.fetchall()

    if(len(result) != 1):
        print('username or password is incorrect')
        return
    
    user = result[0]

    currentUser = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
    
    print(currentUser)

