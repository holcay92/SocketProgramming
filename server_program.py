import socket

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5003  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as an argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many clients the server can listen to simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    while True:
        # receive data stream. It won't accept data packets greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received, break
            break

        # Print the received data
       # print("Server: " + str(data))

        # Check the type of data (temperature or humidity) and print accordingly
        if "Temperature" in data:
            print("Server: " + str(data))
        elif "Humidity" in data:
            print("Server: " + str(data))

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()
