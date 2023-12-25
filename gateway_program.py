import socket
import select
import time
from datetime import datetime, timedelta


def current_time():
    return datetime.now()


def gateway_program():
    host = socket.gethostname()
    gateway_tcp_port = 5001
    gateway_udp_port = 5002
    server_port = 5003

    # Gateway TCP socket for receiving temperature data
    gateway_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gateway_tcp_socket.bind((host, gateway_tcp_port))
    gateway_tcp_socket.listen(1)

    # Initialize last received timestamps for sensors
    last_temp_received_time = current_time()
    last_humidity_received_time = current_time()


    try:
        tcp_conn, tcp_address = gateway_tcp_socket.accept()
        print("Connection from Sensor (TCP): " + str(tcp_address))
    except Exception as e:
        print(f"Error accepting TCP connection: {e}")

    # Gateway UDP socket for receiving humidity data
    gateway_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gateway_udp_socket.bind((host, gateway_udp_port))
    print("Listening for Sensor (UDP) on port " + str(gateway_udp_port))

    # Server socket for forwarding messages to the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, server_port))

    try:
        while True:
            # Use select to wait for either the TCP or UDP socket to be ready
            ready, _, _ = select.select([tcp_conn, gateway_udp_socket], [], [], 3)
            if not ready:
                # Timeout occurred, handle accordingly

                # Check temperature sensor inactivity
                if current_time() - last_temp_received_time > timedelta(seconds=3):
                    server_socket.send("TEMP SENSOR OFF".encode())

                # Check humidity sensor inactivity
                if current_time() - last_humidity_received_time > timedelta(seconds=7):
                    server_socket.send("HUMIDITY SENSOR OFF".encode())
                print(current_time(), last_humidity_received_time)
                # Reset timers
                #last_temp_received_time = current_time()
                #last_humidity_received_time = current_time()

                continue  # Continue waiting for sockets

            for ready_socket in ready:
                if ready_socket is tcp_conn:
                    # Receive temperature data from the sensor via TCP
                    temperature_data = tcp_conn.recv(1024).decode()
                    if not temperature_data:
                        # If data is not received, break
                        break

                    print("Gateway:" + str(temperature_data))
                    # Update the last received time for the temperature sensor
                    last_temp_received_time = current_time()
                    # Forward the temperature data to the server
                    server_socket.send(temperature_data.encode())
                    #print("Temperature data forwarded to Server: " + str(temperature_data))

                elif ready_socket is gateway_udp_socket:
                    # Receive humidity data from the sensor via UDP
                    humidity_data, _ = gateway_udp_socket.recvfrom(1024)
                    if not humidity_data:
                        # If data is not received, break
                        break

                    print("Gateway: " + str(humidity_data))
                    # Update the last received time for the humidity sensor
                    last_humidity_received_time = current_time()
                    # Forward the humidity data to the server
                    server_socket.send(humidity_data)
                    #print("Humidity data forwarded to Server: " + str(humidity_data))

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        tcp_conn.close()
        gateway_udp_socket.close()
        server_socket.close()
        gateway_tcp_socket.close()

if __name__ == '__main__':
    gateway_program()
