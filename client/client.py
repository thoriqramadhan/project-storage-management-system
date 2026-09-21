import socket
from tabulate import tabulate

from client.config import SERVER_HOST, SERVER_PORT
from client.identity import get_client_identity
from client.connection import connect_to_server
from client.menu import display_menu
from client.item_operation import(
    add_item,
    update_stock,
    delete_item
)
from client.health import check_server_health
from services.process_request import show_items





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