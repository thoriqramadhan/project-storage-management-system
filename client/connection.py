import socket
import json

from client.config import SERVER_HOST, SERVER_PORT

def connect_to_server():
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client_socket.connect((SERVER_HOST, SERVER_PORT))

    return client_socket

def send_request(client_socket, action, data):
    request = {
        "action": action,
        "data": data
    }

    request_json = json.dumps(request)

    client_socket.sendall(request_json.encode())

    response = client_socket.recv(4096)

    response_json = response.decode()

    response_data = json.loads(response_json)

    return response_data

