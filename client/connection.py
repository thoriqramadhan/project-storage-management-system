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

    if client_socket is None:
        raise ConnectionError("Client is not connected to server")

    request = {
        "action": action,
        "payload": payload
    }

    request_json = json.dumps(request)

    try:
        client_socket.sendall(request_json.encode("utf-8"))

        buffer = b""

        while True:
            chunk = client_socket.recv(4096)

            if not chunk:
                raise ConnectionError("Server disconnected")

            buffer += chunk

            try:
                response_json = buffer.decode("utf-8")
                response_data = json.loads(response_json)
                break

            except ValueError:
                continue

    except (
        BrokenPipeError,
        ConnectionResetError,
        ConnectionAbortedError,
        TimeoutError,
        OSError
    ) as error:

        raise ConnectionError(
            f"Connection to server lost: {error}"
        )

    # Normalize response
    if "status" in response_data and isinstance(response_data["status"], str):
        response_data["status"] = (
            response_data["status"].lower() in ["success", "sucess"]
        )

    if "message" in response_data and "messages" not in response_data:
        response_data["messages"] = response_data["message"]

    if "data" in response_data and "datas" not in response_data:
        response_data["datas"] = response_data["data"]

    return response_data

