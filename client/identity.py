import socket

def get_client_identity():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return hostname, ip_address
