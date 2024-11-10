import socket
from configs import IP_ADDRESS, PORT
def connect_to_server():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((IP_ADDRESS, PORT))

if __name__ == '__main__':

    connect_to_server()








