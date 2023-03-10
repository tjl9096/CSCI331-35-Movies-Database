import psycopg2; 
# Example credientials file, named .credentials
# <username>
# <password>

#Daniel

# open credential file and read credentials
f = open(".credentials", "r")

username = f.readline()
password = f.readline()

# establishing a connection
connection = psycopg2.connect(
    database="p320_35", 
    user=username, 
    password=password, 
    host='localhost', 
    port='5432'
)

# setting auto commit false
connection.autocommit = False

# get a cursor object
cursor = connection.cursor() 


