import socket
import time
import random
from datetime import datetime


def sensor():
    host = socket.gethostname()  # as both code is running on the same PC
    tcp_port = 5001  # TCP socket server port number
    udp_port = 5002  # UDP socket server port number

    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP client socket
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP client socket

    try:
        tcp_client_socket.connect((host, tcp_port))  # connect to the gateway via TCP

        while True:
            # Temperature Sensor
            temperature_value = random.uniform(20, 30)
            timestamp = time.time()
            formatted_timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            temperature_data = f'Temperature: {temperature_value:.2f}, Timestamp: {formatted_timestamp}'
            tcp_client_socket.send(temperature_data.encode())  # send temperature message
            time.sleep(1)

            # Humidity Sensor
            humidity_value = random.uniform(40, 90)
            if humidity_value > 80:
                formatted_timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                humidity_data = f'Humidity: {humidity_value:.2f}, Timestamp: {formatted_timestamp}'
                udp_client_socket.sendto(humidity_data.encode(), (host, udp_port))  # send humidity message via UDP

            # Send 'ALIVE' message every 3 seconds
            if int(time.time()) % 3 == 0:
                alive_message = "ALIVE"
                udp_client_socket.sendto(alive_message.encode(), (host, udp_port))
    finally:
        tcp_client_socket.close()  # close the TCP connection
        udp_client_socket.close()  # close the UDP connection

if __name__ == '__main__':
    sensor()
