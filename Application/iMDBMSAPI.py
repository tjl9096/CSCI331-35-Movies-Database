# PLEASE READ:
#
# This will be the file that run the main function. 
# Avoid adding code here, create another file with 
# functions that return SQL code. Edit this file only
# to call your functions (or if there is a bug). 
#

import psycopg2
from sshtunnel import SSHTunnelForwarder
from UserCommands import *


# connects to the server and runs commands 
def main():
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

            # This loop will run
            # conn and curs are passed so that you can run SQL commands 
            while True:
                result = runCommand(conn, curs)
                if result == 'stop':
                    break

            conn.close()
    except Exception as exception:
        print("Connection failed")
        print(exception)
        
        
# reads from the console, runs the correct code
#
# console input will be as follows 
#
# [command] [arg1] [arg2] [arg3]
# 
# write your function calls in this function
def runCommand(conn, curs):
    # read user input
    input_line = input('iMDBMS command >> ')
    # split line on spaces 
    split_line = input_line.split(' ')

    # parse the input
    # convert everything to lowercase 
    command = split_line[0].lower()
    args = [arg.lower() for arg in split_line[1:]]


    # ============== QUICK START INFO ==========================
    #
    # call your functions using the switch statment below, 
    # make up a command, *add it to the displayCommands function*
    # 
    # at this point in the code you have 
    # conn - used to execute SQL commands
    # curs - used to execute SQL commands 
    # command - the command typed in by the user (lowercase)
    # args - a string array of args typed by the user (lowercase)

    # =============== STUDENT CODE BLOCK STARTS HERE ============
    # =============== (obviously im joking) =====================
    # =============== (this was all written by a student) =======

    match command:
        # add your commands here
        case 'getuser':
            getUser(conn, curs, args)
        case 'list':
            displayCommands()
        case 'help':
            displayUsage()
        case 'stop':
            return 'stop' 
        # default 
        case _:
            displayUsage()

    # =============== STUDENT CODE BLOCK ENDS HERE ===============


def displayUsage():
    print('Usage: [command] [arg1] [arg2] [...]')
    print('list shows all functions')
    print('stop will stop the program')
    print()


def displayCommands():
    displayUsage()
    print('---------- Commands ----------')
    getUserUsage()
    # add more commands here
    print()


if __name__ == "__main__":
    main()