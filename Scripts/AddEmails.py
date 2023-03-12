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

def getRandomEmails(user_id, user_username, num_emails):
    emailEndings = ["@gmail.com", "@yahoo.com", "@outlook.com", "@email.com", "@post.com", "@usa.com"]
    val = ''
    for i in range(num_emails):
        val = val + "("
        val = val + str(user_id) + ', '
        choice = random.choice(emailEndings)
        emailEndings.remove(choice)
        val = val + '\'' + str(user_username) + choice + '\'' + ')'
        if i + 1 != num_emails:
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
        with open("Scripts/UserMockData.csv", "r") as dataFile:
            for line in dataFile:
                splitLine = line.split(",")
                user_id = splitLine[0]
                user_username = splitLine[2]
                
                # User has a 1/5 chance of not having any emails 
                num_emails = random.randint(0, 4)

                if(num_emails != 0):
                    curs.execute(f'INSERT INTO \"Email\" (user_id, email) VALUES {getRandomEmails(user_id, user_username, num_emails)}')

        print("Successful inserted")
        conn.commit()
        conn.close()
except Exception as exception:
    print("Connection failed")
    print(exception)



