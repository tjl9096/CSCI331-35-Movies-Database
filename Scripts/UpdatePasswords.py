import hashlib
import psycopg2
from sshtunnel import SSHTunnelForwarder

f = open('Scripts/.credentials', 'r')

username = f.readline().replace('\n', '')
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
        for user_id in range(1, 105):
            curs.execute('SELECT user_id, password FROM \"User\" WHERE user_id = ' + str(user_id))
            result = curs.fetchall()
            new_password = str(result[0][1])
            new_password = new_password.encode()
            new_password = hashlib.sha3_256(new_password)
            curs.execute('UPDATE \"User\" set password = \'' + str(new_password.hexdigest()) + '\' where user_id = ' + str(user_id))

        print("Successful inserted")
        conn.commit()
        conn.close()
except Exception as exception:
    print("Connection failed")
    print(exception)
