import psycopg2
import random
from sshtunnel import SSHTunnelForwarder
# Example credientials file, named .credentials
# <username>
# <password>

# open credential file and read credentials
f = open('Scripts/.credentials', "r")

username = f.readline().replace("\n", "")
password = f.readline()


# lol, get some friends bc you have none 
def getFriends(user_id, numFriends):
    possibilities = list(range(1, 101))
    val = ''
    for i in range(numFriends):
        # get the friend Id
        friend_id = random.choice(possibilities)
        # remove it from possibilities to avoid duplicate data
        possibilities.remove(friend_id)
        val = val + '(' + str(user_id) + ', ' + str(friend_id) + ')'
        if i + 1 != numFriends:
            val = val + ', '
    return val


try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('localhost', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'database': 'p320_35',
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }


        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")
        for user_id in range(1, 101):
            
            # User has a 1/10 chance of not having any emails 
            has_friends = random.randint(0, 9)
            numFriends = random.randint(0, 25)

            if(numFriends != 0):
                curs.execute(f'INSERT INTO \"Friends\" (user_id, friend_id) VALUES {getFriends(user_id, numFriends)}')

        print("Successful inserted")
        conn.commit()
        conn.close()
except Exception as exception:
    print("Connection failed")
    print(exception)