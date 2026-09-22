import time

from client.connection import send_request

from tabulate import tabulate

def check_server_health(client_socket):
    print("\n=== STATUS SERVER ===")
    print("Fitur sementara dinonaktifkan.")
    pass

def show_access_logs(client_socket):
    print("\n=== LOG AKSES SERVER ===")
    response = send_request(client_socket, "GET_ACCESS_LOGS", {})

    if response.get("status") is True:
        logs = response.get("datas") or []
        if not logs:
            print("Tidak ada data log akses.")
            return

        table = []
        for log in logs:
            if isinstance(log, (list, tuple)):
                table.append([log[0], log[1], log[2], log[3], log[4]])
            else:
                table.append([
                    log.get("id"),
                    log.get("client_ip"),
                    log.get("client_hostname"),
                    log.get("action_performed"),
                    log.get("created_at")
                ])

        print(tabulate(table, headers=["ID", "Client IP", "Hostname", "Action", "Waktu"], tablefmt="grid"))
    else:
        print("\nGagal:", response.get("messages", "Terjadi kesalahan"))
