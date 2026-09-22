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

def send_request(client_socket, action, payload):
    request = {
        "action": action,
        "payload": payload
    }

    request_json = json.dumps(request)

    client_socket.sendall(request_json.encode("utf-8"))

    response = client_socket.recv(4096)
    
    # Debug: print the raw response
    print(f"DEBUG: raw response from server: {repr(response)}")

    response_json = response.decode("utf-8")

    response_data = json.loads(response_json)

    return response_data

