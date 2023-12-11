import socket
import select

def gateway_program():
    # client socket
    host = socket.gethostname()
    port = 5001

    gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gateway_socket.bind((host, port))
    gateway_socket.listen(1)
    conn, address = gateway_socket.accept()
    print("Connection from: " + str(address))

    # server socket
    server_host = socket.gethostname()
    server_port = 5002

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_host, server_port))

    while True:
        # Use select to set a timeout for receiving data from the client
        ready, _, _ = select.select([conn], [], [], 3)
        if not ready:
            # Timeout occurred, send an error message to the server
            error_message = "ERROR: No message received from client within 3 seconds."
            server_socket.send(error_message.encode())
            print(error_message)
            continue

        # Receive data from the client
        sensor_message = conn.recv(1024).decode()
        if not sensor_message:
            # If data is not received, break
            break

        print("Sensor data sent to gateway: " + str(sensor_message))
        server_socket.send(sensor_message.encode())
        print("Gateway data sent to server: " + str(sensor_message))

    conn.close()
    server_socket.close()

if __name__ == '__main__':
    gateway_program()
