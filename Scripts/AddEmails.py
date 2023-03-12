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
        with open("Scripts/UserMockData.csv", "r") as dataFile:
            for line in dataFile:
                splitLine = line.split(",")
                if(splitLine[1] < splitLine[6]): 
                    splitLine[1] = splitLine[6]
                curs.execute(f'INSERT INTO \"User\"(user_id, last_access_date, username, password, first_name, last_name, creation_date) VALUES ({splitLine[0]}, \'{splitLine[1]}\', \'{splitLine[2]}\', \'{splitLine[3]}\', \'{splitLine[4]}\', \'{splitLine[5]}\', \'{splitLine[6]}\')')

        print("Successful inserted")
        conn.commit()
        conn.close()
except Exception as exception:
    print("Connection failed")
    print(exception)


getRandomEmail(username):
    emailEndings = ["@gmail.com", "@yahoo.com", "@outlook.com", "@email.com", "@post.com", "@usa.com", ""]
