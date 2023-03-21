'''
author:         Hoja Arzanesh

description:    takes the csv file containing shuffled movie_ids (1-100)
                and shuffled contributor_ids (1-100) outputs them into
                acts, directs, produces csv files.
'''

import csv
import random


with open('ActsDirectsProducesMockData.csv', 'r') as inp, open('ActsMockDataVersion2.csv', 'a') as outp1, open('DirectsMockDataVersion2.csv', 'a') as outp2, open('ProducesMockDataVersion2.csv', 'a') as outp3:
    acts_writer = csv.writer(outp1)
    directs_writer = csv.writer(outp2)
    produces_writer = csv.writer(outp3)

    # has_header = csv.Sniffer().has_header(inp.read(1024))
    reader = csv.reader(inp, delimiter=",")
    reader_list = list(reader)
    needed_list = reader_list[1:]

    numbers = []
    for i in range (1, 101):
        numbers.append(i)

    random.shuffle(numbers)

    acts_pool = []
    for i in range (0, 55):
        acts_pool.append(numbers[i])
    
    print(acts_pool)

    acts_writer.writerow(['movie_id', 'contributor_id'])

    # fill up acts csv file
    for i in range(1, 101):
        num_actors = random.randrange(0, 5)    # num_actors = number of actors

        for j in range(0, num_actors):
            row = [i, acts_pool[j]]
            acts_writer.writerow(row)
        
        random.shuffle(acts_pool)

        # id_id = str(row[0]) + ',' + str(row[1])
    
    directs_pool = []
    for i in range (0, 15):
        directs_pool.append(numbers[55 + i])
    
    print(directs_pool)

    directs_writer.writerow(['movie_id', 'contributor_id'])

    for i in range (1, 101):
        row = [i, random.choice(directs_pool)]
        directs_writer.writerow(row)
    
    produces_pool = []
    for i in range(0, 30):
        produces_pool.append(numbers[55 + 15 + i])
    
    print(produces_pool)

    produces_writer.writerow(['movie_id', 'contributor_id'])

    for i in range(1, 101):
        num_producers = random.randrange(1, 4) # max 3 producers

        for j in range(0, num_producers):
            row = [i, produces_pool[j]]
            produces_writer.writerow(row)

        random.shuffle(produces_pool)
    

    
    # random_numbers = []
    # for i in range (0, 100):
    #     random_numbers.append(random.randrange())
    # # fill up directs csv file
    # for i in range(0, 100):
    #     random.shuffle(needed_list)
    #     row = needed_list.pop()

    #     # id_id = str(row[0]) + ',' + str(row[1])

    #     directs_writer.writerow(row)
    #     directs_writer.
    
    # # fill up produces csv file
    # for i in range(0, 30):
    #     random.shuffle(needed_list)
    #     row = needed_list.pop()

    #     # id_id = str(row[0]) + ',' + str(row[1])

    #     produces_writer.writerow(row)

    # print(needed_list)
    # # chosen_row = random.choice(list(reader))