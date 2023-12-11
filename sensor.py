import socket
import time
import random


def sensor():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5001  # socket server port number

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the gateway


    while True:
        temperature_value = random.uniform(20, 30)
        timestamp = time.time()
        data = f'Temperature: {temperature_value}, Timestamp: {timestamp}'
        client_socket.send(data.encode())  # send message
        time.sleep(4)
    client_socket.close()  # close the connection


if __name__ == '__main__':
    sensor()
