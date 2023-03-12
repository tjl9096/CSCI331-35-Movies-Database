# Console application to access the database 


def displayUsage():
    print('Usage: [command] [arg1] [arg2] [...]')
    print('list shows all functions')
    print('stop will stop the program')
    print()


def displayCommands():
    displayUsage()
    print('---------- Commands ----------')

    # add more commands here
    print()


# reads from the console, runs the correct code
#
# console input will be as follows 
#
# [command] [arg1] [arg2] [arg3]
# 
def main():
    while True: 
        # read user input
        input_line = input('iMDBMS command >> ')
        # split line on spaces 
        split_line = input_line.split(' ')

        # parse the input
        # convert everything to lowercase 
        command = split_line[0].lower()
        args = [arg.lower() for arg in split_line[1:]]

        match command:

            case 'list':
                displayCommands()
            case 'help':
                displayUsage()
            case 'stop':
                break 
            # default 
            case _:
                displayUsage()
        
        







if __name__ == "__main__":
    main()