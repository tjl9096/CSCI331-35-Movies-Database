'''
author:         Hoja Arzanesh

description:    takes the csv file containing shuffled movie_ids (1-100)
                and shuffled contributor_ids (1-100) outputs them into
                acts, directs, produces csv files.
'''

import csv
import random


with open('ActsDirectsProducesMockData.csv', 'r') as inp, open('ActsMockData.csv', 'a') as outp1, open('DirectsMockData.csv', 'a') as outp2, open('ProducesMockData.csv', 'a') as outp3:
    acts_writer = csv.writer(outp1)
    directs_writer = csv.writer(outp2)
    produces_writer = csv.writer(outp3)

    # has_header = csv.Sniffer().has_header(inp.read(1024))
    reader = csv.reader(inp, delimiter=",")
    reader_list = list(reader)
    needed_list = reader_list[1:]

    # fill up acts csv file
    for i in range(0, 55):
        random.shuffle(needed_list)
        row = needed_list.pop()

        print(row)

        # id_id = str(row[0]) + ',' + str(row[1])

        acts_writer.writerow(row)
    
    # fill up directs csv file
    for i in range(0, 15):
        random.shuffle(needed_list)
        row = needed_list.pop()

        # id_id = str(row[0]) + ',' + str(row[1])

        directs_writer.writerow(row)
    
    # fill up produces csv file
    for i in range(0, 30):
        random.shuffle(needed_list)
        row = needed_list.pop()

        # id_id = str(row[0]) + ',' + str(row[1])

        produces_writer.writerow(row)

    print(needed_list)
    # chosen_row = random.choice(list(reader))