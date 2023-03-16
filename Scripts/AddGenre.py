import psycopg2
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
        with open("./GenreMockData.csv", "r") as dataFile:
            dataFile.readline()
            for line in dataFile:
                line = line.strip()
                splitLine = line.split(",")
                genre_id = int(splitLine[0])
                genre_name = splitLine[1]
                
                curs.execute(f'INSERT INTO \"Genre\" (Genre_ID, Genre_Name) VALUES {genre_id,genre_name}')

        print("Successful inserted")
        conn.commit()
        conn.close()
except Exception as exception:
    print("Connection failed")
    print(exception)