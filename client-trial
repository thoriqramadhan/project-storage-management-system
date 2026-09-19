import socket
import json
import time

from tabulate import tabulate

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

def get_client_identity():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return hostname, ip_address

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


def display_menu():
    print("\n====================================")
    print("      STORAGE MANAGEMENT CLIENT")
    print("====================================")
    print("1. Lihat Stok Barang")
    print("2. Tambah Barang")
    print("3. Update Stok")
    print("4. Hapus Barang")
    print("5. Cek Status Server")
    print("6. Keluar")
    print("====================================")


def show_items(client_socket):
    print("\n=== DAFTAR BARANG ===")

    response = send_request(
        client_socket,
        "GET_ITEMS",
        {}
    )

    if response["status"] == "OK":

        items = response["data"]

        if not items:
            print("Tidak ada data barang.")
            return

        table = []

        for item in items:
            table.append([
                item["id"],
                item["name"],
                item["category"],
                item["stock"],
                item["unit"]
            ])

        print(
            tabulate(
                table,
                headers=[
                    "ID",
                    "Barang",
                    "Kategori",
                    "Stock",
                    "Unit"
                ],
                tablefmt="grid"
            )
        )

    else:
        print("Gagal:", response["message"])


def add_item(client_socket):
    print("\n=== TAMBAH BARANG ===")

    name = input("Nama barang   : ")
    category_id = input("ID kategori   : ")
    stock = input("Stock         : ")
    unit = input("Unit          : ")

    # Validasi input
    if not name:
        print("Nama barang tidak boleh kosong.")
        return

    try:
        category_id = int(category_id)
        stock = int(stock)
    except ValueError:
        print("ID kategori dan stock harus berupa angka.")
        return

    if stock < 0:
        print("Stock tidak boleh negatif.")
        return

    data = {
        "name": name,
        "category_id": category_id,
        "stock": stock,
        "unit": unit
    }

    response = send_request(
        client_socket,
        "ADD_ITEM",
        data
    )

    if response["status"] == "OK":
        print("\nBarang berhasil ditambahkan.")
    else:
        print("\nGagal:", response["message"])

def update_stock(client_socket):
    print("\n=== UPDATE STOCK ===")

    item_id = input("ID barang  : ")
    stock = input("Stock baru : ")

    try:
        item_id = int(item_id)
        stock = int(stock)
    except ValueError:
        print("ID barang dan stock harus berupa angka.")
        return

    if stock < 0:
        print("Stock tidak boleh negatif.")
        return

    data = {
        "item_id": item_id,
        "stock": stock
    }

    response = send_request(
        client_socket,
        "UPDATE_STOCK",
        data
    )

    if response["status"] == "OK":
        print("\nStock berhasil diperbarui.")
    else:
        print("\nGagal:", response["message"])

def delete_item(client_socket):
    print("\n=== HAPUS BARANG ===")

    item_id = input("ID barang yang akan dihapus: ")

    try:
        item_id = int(item_id)
    except ValueError:
        print("ID barang harus berupa angka.")
        return

    confirm = input("Yakin ingin menghapus? (y/n): ")

    if confirm.lower() != "y":
        print("Penghapusan dibatalkan.")
        return

    data = {
        "item_id": item_id
    }

    response = send_request(
        client_socket,
        "DELETE_ITEM",
        data
    )

    if response["status"] == "OK":
        print("\nBarang berhasil dihapus.")
    else:
        print("\nGagal:", response["message"])


def check_server_health(client_socket):
    print("\n=== STATUS SERVER ===")

    start_time = time.time()

    response = send_request(
        client_socket,
        "CHECK_HEALTH",
        {}
    )

    end_time = time.time()

    latency = (end_time - start_time) * 1000

    if response["status"] == "OK":

        data = response["data"]

        print("------------------------------------")
        print("Server Status :", data["status"])
        print("Server IP     :", data["ip"])
        print("CPU Usage     :", data["cpu"], "%")
        print("RAM Usage     :", data["ram"], "%")
        print("Latency       :", round(latency, 2), "ms")
        print("------------------------------------")

    else:
        print("\nGagal:", response["message"])


def main():

    hostname, ip_address = get_client_identity()

    print("\n====================================")
    print("      STORAGE MANAGEMENT CLIENT")
    print("====================================")
    print("Hostname :", hostname)
    print("IP       :", ip_address)

    print("\nConnecting to server...")
    print(
        "Server   :",
        SERVER_HOST,
        ":",
        SERVER_PORT
    )

    try:
        client_socket = connect_to_server()

    except ConnectionRefusedError:
        print("\nGagal terhubung ke server.")
        print("Pastikan server.py sedang berjalan.")
        return

    except socket.timeout:
        print("\nKoneksi ke server timeout.")
        return

    except OSError as error:
        print("\nConnection error:", error)
        return

    print("Connected to server!")


    while True:

        display_menu()

        choice = input("Pilih menu: ")

        if choice == "1":
            show_items(client_socket)

        elif choice == "2":
            add_item(client_socket)

        elif choice == "3":
            update_stock(client_socket)

        elif choice == "4":
            delete_item(client_socket)

        elif choice == "5":
            check_server_health(client_socket)

        elif choice == "6":
            print("\nDisconnecting...")

            client_socket.close()

            print("Client ditutup.")
            break

        else:
            print("\nPilihan tidak valid.")
            print("Silakan pilih menu 1-6.")


if __name__ == "__main__":
    main()