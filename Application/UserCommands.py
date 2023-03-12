
def getUserUsage():
    print('Usage: getuser [user_id] ')


def getUser(conn, curs, args):
    if len(args) != 1:
        getUserUsage()
        return
    
    user_id = args[0]
    sqlCommand = 'SELECT * FROM \"User\" WHERE user_id = ' + str(user_id)
    curs.execute(sqlCommand)
    result = curs.fetchall()
    print(result)