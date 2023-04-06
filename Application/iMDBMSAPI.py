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
from CollectionCommands import *
from RatingCommands import *
from watchCommands import *


# connects to the server and runs commands 
def main():

    printFrog()

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
    input_line = input('iMDBMS FROG >> ')
    # split line on spaces 
    split_line = input_line.split(' ')

    # parse the input
    # convert everything to lowercase 
    command = split_line[0].lower()
    args = split_line[1:]


    # ============== QUICK START INFO ==========================
    #
    # call your functions using the switch statment below, 
    # make up a command, *add it to the displayCommands function*
    # 
    # at this point in the code you have 
    # conn - used to execute SQL commands
    # curs - used to execute SQL commands 
    # command - the command typed in by the user (lowercase)
    # args - a string array of args typed by the user

    # =============== STUDENT CODE BLOCK STARTS HERE ============
    # =============== (obviously im joking) =====================
    # =============== (this was all written by a student) =======

    match command:
        # add your commands here
        case 'search_movies':
            searchMovie(curs)
        case 'search_friends':
            searchFriends(curs)
        case 'searchfriends':
            searchFriends(curs)
        case 'list_friends':
            listFriends(curs)
        case 'listfriends':
            listFriends(curs)
        case 'listtotalfriends':
            listTotalFriends(curs)
        case 'list_total_friends':
            listTotalFriends(curs)
        case 'list_friended_me':
            listFriendedMe(curs)
        case 'listfriendedme':
            listFriendedMe(curs)
        case 'list_total_friended_me':
            listTotalFriendedMe(curs)
        case 'listtotalfriendedme':
            listTotalFriendedMe(curs)
        case 'add_friend':
            addFriend(curs, conn)
        case 'addfriend':
            addFriend(curs, conn)
        case 'remove_friend':
            removeFriend(curs, conn)
        case 'removefriend':
            removeFriend(curs, conn)
        case 'get_user':
            getUser(curs)
        case 'getuser':
            getUser(curs)
        case 'login':
            login(curs, conn)
        case 'logout':
            logout()
        case 'create_account':
            createAccount(curs, conn)
        case 'createaccount':
            createAccount(curs, conn)
        case 'search_friends':
            searchFriends(curs)
        case 'searchfriends':
            searchFriends(curs)
        case 'create_collection':
            createCollection(curs, conn)
        case 'createcollection':
            createCollection(curs, conn)
        case 'list_collections':
            listCollections(curs)
        case 'listcollections':
            listCollections(curs)
        case 'list_total_collections':
            listTotalCollections(curs)
        case 'listtotalcollections':
            listTotalCollections(curs)
        case 'rename_collection':
            renameCollection(curs, conn)
        case 'renamecollection':
            renameCollection(curs, conn)
        case 'delete_collection':
            deleteCollection(curs, conn)
        case 'deletecollection':
            deleteCollection(curs, conn)
        case 'view_collection':
            viewCollection(curs)
        case 'viewcollection':
            viewCollection(curs)
        case 'add_movie_to_collection':
            addMovieToCollection(curs, conn)
        case 'addmovietocollection':
            addMovieToCollection(curs, conn)
        case 'remove_movie_from_collection':
            removeMovieFromCollection(curs, conn)
        case 'removemoviefromcollection':
            removeMovieFromCollection(curs, conn)
        case 'rate_movie':
            rateMovie(curs, conn)
        case 'ratemovie':
            rateMovie(curs, conn)
        case 'getmytop10':
            top10Movies(curs)
        case 'get_my_top_10':
            top10Movies(curs)
        case 'getmoviesofthemonth':
            top_five_month(curs)
        case 'get_movies_of_the_month':
            top_five_month(curs)
        case 'watch_movie':
            watchMovie(curs, conn)
        case 'watchmovie':
            watchMovie(curs, conn)
        case 'watch_collection':
            watchCollection(curs, conn)
        case 'watchcollection':
            watchCollection(curs, conn)
        case 'forme':
            forMe(curs)
        case 'for_me':
            forMe(curs)
        case 'top_20_recommend':
            top20Recommends(curs)
        case 'top20recommend':
            top20Recommends(curs)
        case 'list':
            displayCommands()
        case 'help':
            displayUsage()
        case 'stop':
            return 'stop' 
        case 'quit':
            return 'stop'
        case 's':
            return 'stop'
        case 'q':
            return 'stop'
        # default 
        case _:
            displayUsage()

    # =============== STUDENT CODE BLOCK ENDS HERE ===============


def displayUsage():
    print('Usage: [command]')
    print('command "list" shows all functions')
    print('command "stop" will stop the program')
    print()


def displayCommands():
    displayUsage()
    print('---------- Commands ----------')
    print('list_friended_me')
    print('list_total_friended_me')
    print('list_friends')
    print('list_total_friends')
    print('search_friends')
    print('add_friend')
    print('remove_friend')
    print('get_user')
    print('login')
    print('logout')
    print('create_account')
    print('search_friends')
    print('create_collection')
    print('list_total_collections')
    print('list_collections')
    print('rename_collection')
    print('delete_collection')
    print('view_collection')
    print('add_movie_to_collection')
    print('remove_movie_from_collection')
    print('rate_movie')
    print('get_my_top_10')
    print('top_20_recommend')
    print('get_movies_of_the_month')
    print('watch_movie')
    print('watch_collection')
    print('for_me')
    print('list')
    print('help')
    print('stop')
    # add more commands here
    print()


def printFrog():
    print(
'''   


                                                   ##(#             
                                              (&%&%&&%&&%#(         
         (%&&&&%&%&%&&,                     %#%###%#%%#&@@@@&,      
        %&&@&(%%&%#%###%%               .%%%#%(&&#####&@@@@#. *     
      ##&@@@@@%(%(/((%&&%%&&&&&&&&&&&&&&&&&&&&%##%#%#*,, .     *    
         ,,  .*/##(///#&#%%&&&&&&&%&&&&&&%%%%%%#(%##(.,*,/(//((/    
     .*((((/,,,.(%#(#/###%(/%%%&%%%%%%%%%#(%%%%%%#(##(,,////(((     
      (///////.,(#%#%###((((##%%%%%%%%%%##(((#####%#%%%(.,*///      
       //*/// /((##(#(((/((###%%%%%%%%#%%#%##%%%%%#%##(((((((((/    
       #/,,*((((%%#%%%%#####%##%#((((##%%%%%##%%%%%#%%%%########(   
      *(////((%###(####(####((((//////(/(((((####((##########%%%&&@@
     ,/#((##((/(#(((##((((///////****/////////(((((((((((((/////((%%##,                       
     &####((((//(////////******,,,,,,,,,,,,,****//((###((((((////(##(###&&&@&&@%@@&@          
    #/*,/////////*///////*******,*,*****,**,,,*,,*,,,,,,,,,...,*(&&&@&%&&@@&&&%%#%%%%%%       
   %#//**********,,,,,,,,,,,,,,,****,*,,,,,,,.,,..*((#%@&%#(/%%&@&&&&&@@@&&&%##(#%%%%%%&&     
 %&#(#%#%&&&&%/,,,,,,,,,,,,...,,...........,,,.(%&&@&&&&&&&%%%%%(/,/#%%%&&#*****//((###(#%    
 #(#(#%&&&&&&%(*,,,..,,,,*,,******,,,.......,..,(%%%%%%#//(/////*/*/#%%####                   
        ...     
                
                
'''
)

if __name__ == "__main__":
    main()