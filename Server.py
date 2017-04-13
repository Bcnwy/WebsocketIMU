import csv
import json
from datetime import datetime
from time import time

from websocket_server import WebsocketServer

_file_Quaterion = ("{}-Quaterion.csv".format(datetime.now().date()))
_file_IMU = ("{}-IMU.txt".format(datetime.now().date()))
start_time = 0


def new_client(client, server):
    print("Hey all, a new client has joined us")
    # start of EPOCH time
    global start_time
    start_time = time()


def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    # print("Client(%d) said: %s" % (client['id'], message))
    print(message)
    data = json.loads(message)

    #print(data['Accelerometer'])

    if 'Accelerometer' in data:
        # Get read time
        read_time = time()-start_time
        with open(_file_IMU, 'a') as File:
            write = csv.writer(File, dialect='excel')
            # write a new row the the csv file
            write.writerow([
                data['Accelerometer']['x'],
                data['Accelerometer']['y'],
                data['Accelerometer']['z'],
                data['Time'],
                str(read_time)])

    if 'Quaterion' in data:
        # Get read time
        read_time = time() - start_time
        with open(_file_Quaterion, 'ab') as File:
            write = csv.writer(File, dialect='excel')
            # write a new row the the csv file
            write.writerow([data['Quaterion']['w'], str(read_time)])


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


if __name__ == '__main__':
    with open(_file_Quaterion, 'w') as csvFile:
        writer = csv.writer(csvFile, dialect='excel')
        # write a new row the the csv file
        writer.writerow([str.format('{0}', datetime.now())])
        header = "W", "X", "Y", "Z", "TIME"
        writer.writerow(header)

    with open(_file_IMU, 'w') as csvFile:
        writer = csv.writer(csvFile, dialect='excel')
        # write a new row the the csv file
        writer.writerow([str.format('{0}', datetime.now())])
        header = "X", "Y", "Z", "TIME"
        writer.writerow(header)

    server = WebsocketServer(81, host='0.0.0.0')
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
