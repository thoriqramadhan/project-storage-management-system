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
            # Continue reading if JSON is incomplete or UTF-8 decoding fails on boundary
            continue
            
    # Debug: print the raw response
    # print(f"DEBUG: raw response string length: {len(buffer)}")

    # Normalize response to handle changes from the server API
    if "status" in response_data and isinstance(response_data["status"], str):
        response_data["status"] = True if response_data["status"].lower() == "sucess" or response_data["status"].lower() == "success" else False
        
    if "message" in response_data and "messages" not in response_data:
        response_data["messages"] = response_data["message"]
        
    if "data" in response_data and "datas" not in response_data:
        response_data["datas"] = response_data["data"]

    return response_data

