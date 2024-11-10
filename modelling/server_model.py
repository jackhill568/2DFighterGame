import socket
import time

from configs import IP_ADDRESS, PORT
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP_ADDRESS, PORT))
s.listen(10)
wait = True
clients = []


def setup():

    client_connection, client_address = s.accept()
    clients.append((client_connection, client_address))
    print("new connection at ", client_address)
    print("connection success")


if __name__ == '__main__':
    setup()
    s.close()
