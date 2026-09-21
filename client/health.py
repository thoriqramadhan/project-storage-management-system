import time

from client.connection import send_request

def check_server_health(client_socket):
    print("\n=== STATUS SERVER ===")

    start_time = time.time()

    response = send_request(
        client_socket,
        "CHECK_SERVER_STATUS",
        {}
    )

    end_time = time.time()

    latency = (end_time - start_time) * 1000

    if response["status"] is True:

        data = response["datas"]

        print("------------------------------------")
        print("Server Status :", data["status"])
        print("Server IP     :", data["ip"])
        print("CPU Usage     :", data["cpu"], "%")
        print("RAM Usage     :", data["ram"], "%")
        print("Latency       :", round(latency, 2), "ms")
        print("------------------------------------")

    else:
        print("\nGagal:", response["messages"])
