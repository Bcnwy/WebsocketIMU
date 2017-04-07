from websocket_server import WebsocketServer
from time import time
from datetime import datetime
import csv
import logging

_file = ("{}-ABS_IMU.csv".format(datetime.now().date()))
start_time = 0


def new_client(client, server):
    print("Hey all, a new client has joined us")
    # start of EPOCH time
    global start_time
    start_time = time()


def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))
    # Get read time
    read_time = time()-start_time
    with open(_file, 'a') as File:
        write = csv.writer(File, dialect='excel')
        # write a new row the the csv file
        # TODO Handle json formatted data before saving
        write.writerow([message, str(read_time)])


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


if __name__ == '__main__':
    with open(_file, 'w') as csvFile:
        writer = csv.writer(csvFile, dialect='excel')
        # write a new row the the csv file
        writer.writerow([str.format('{0}', datetime.now())])

    server = WebsocketServer(81, host='0.0.0.0')
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
