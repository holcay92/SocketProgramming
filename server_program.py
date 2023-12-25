import socket
from flask import Flask, render_template_string

app = Flask(__name__)
# Store received data in lists
temperature_data_list = []
humidity_data_list = []


def server_program():
    host = socket.gethostname()
    port_socket = 5003
    port_web = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port_socket))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()

        # Print the received data
        print("Server: " + str(data))

        # Store data in the respective lists
        if "TEMP" in data and "HUMIDITY" not in data:
            temperature_data_list.append(str(data))
        elif "HUMIDITY" in data and "TEMP" not in data:
            humidity_data_list.append(str(data))


    conn.close()


@app.route('/')
def index():
    return render_template_string('''
        <h1>Welcome to the Sensor Data Dashboard</h1>
        <ul>
            <li><a href="/temperature">Temperature Data</a></li>
            <li><a href="/humidity">Humidity Data</a></li>
        </ul>
    ''')


@app.route('/temperature')
def temperature():
    return render_template_string('''
        <h1>Temperature Data</h1>
        <ul>
            {% for data in temperature_data_list %}
                <li>{{ data }}</li>
            {% endfor %}
        </ul>
        <p><a href="/">Go back to Dashboard</a></p>
    ''', temperature_data_list=temperature_data_list)


@app.route('/humidity')
def humidity():
    return render_template_string('''
        <h1>Humidity Data</h1>
        <ul>
            {% for data in humidity_data_list %}
                <li>{{ data }}</li>
            {% endfor %}
        </ul>
        <p><a href="/">Go back to Dashboard</a></p>
    ''', humidity_data_list=humidity_data_list)


if __name__ == '__main__':
    # Run the Flask app in a separate thread
    from threading import Thread

    web_thread = Thread(target=app.run, kwargs={'host': 'localhost', 'port': 8080})
    web_thread.start()

    # Run the server program
    server_program()
