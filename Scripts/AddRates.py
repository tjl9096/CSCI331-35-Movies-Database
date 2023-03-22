import psycopg2
import random
from faker import Faker
from datetime import datetime
from sshtunnel import SSHTunnelForwarder
# Example credientials file, named .credentials
# <username>
# <password>

# open credential file and read credentials
f = open('Scripts/.credentials', "r")

username = f.readline().replace("\n", "")
password = f.readline()

fake = Faker()
Dates = {}
while len(Dates) <= 1000:
    Dates[fake.date_between(datetime(2022,1,1), datetime(2024,12,31))] = 0


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

        for date_obj in Dates.keys():
            date = date_obj.strftime("%Y-%m-%d")
            user_id = random.randint(1, 100)
            movie_id = random.randint(1, 100)
            rating = random.randint(1,5)
            curs.execute(f'INSERT INTO \"Rates\"(user_id, movie_id, rating, date) VALUES {user_id, movie_id, rating, date}')

        print("Successful inserted")
        conn.commit()
        conn.close()
except Exception as exception:
    print("Connection failed")
    print(exception)