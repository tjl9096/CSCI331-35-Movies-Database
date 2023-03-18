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
        with open("./CollectionContainsMockData.csv", "r") as dataFile:
            for line in dataFile:
                splitLine = line.split(",")
                user_id = splitLine[0]
                collection_id = splitLine[1]
                num_movies = random.randint(0,10)
                possibilities = list(range(1,101))

                for _ in range(0, num_movies):
                    movie_id = random.choice(possibilities)
                    possibilities.remove(movie_id)
                    curs.execute(f'INSERT INTO \"Collection_Contains\"(user_id, collection_id, movie_id) VALUES {user_id, collection_id, movie_id}')

        print("Successful inserted")
        conn.commit()
        conn.close()
except Exception as exception:
    print("Connection failed")
    print(exception)
