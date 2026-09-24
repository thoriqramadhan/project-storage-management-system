import os
import sys

# Add project root to sys.path and remove script dir to prevent module shadowing
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

import socket

from client.config import SERVER_HOST, SERVER_PORT
from client.identity import get_client_identity
from client.connection import connect_to_server

from client.menu import (
    display_main_menu,
    display_item_menu,
    display_rack_menu,
    display_category_menu,
    display_system_menu
)

from client.item_operation import (
    add_item,
    update_stock,
    delete_item
)

from services.process_request import show_items

from client.rack_operation import (
    show_racks,
    add_rack,
    edit_rack,
    delete_rack
)

from client.category_operation import (
    show_categories,
    add_category,
    edit_category,
    delete_category
)

from client.health import (
    check_server_health,
    show_access_logs
)



def item_loop(client_socket):
    while True:
        display_item_menu()
        choice = input("Pilih menu barang: ")

        # Kembali ke menu utama
        if choice == "5":
            return client_socket

        try:
            if choice == "1":
                show_items(client_socket)

            elif choice == "2":
                add_item(client_socket)

            elif choice == "3":
                update_stock(client_socket)

            elif choice == "4":
                delete_item(client_socket)

            else:
                print("\nPilihan tidak valid.")

        except ConnectionError:
            print("\nServer terputus.")

            # Reconnect
            client_socket = connect_with_retry()

def rack_loop(client_socket):
    while True:
        display_rack_menu()
        choice = input("Pilih menu rak: ")

        # Kembali ke menu utama
        if choice == "5":
            return client_socket

        try:
            if choice == "1":
                show_racks(client_socket)

            elif choice == "2":
                add_rack(client_socket)

            elif choice == "3":
                edit_rack(client_socket)

            elif choice == "4":
                delete_rack(client_socket)

            else:
                print("\nPilihan tidak valid.")

        except ConnectionError:
            print("\nServer terputus.")

            # Reconnect
            client_socket = connect_with_retry()

def category_loop(client_socket):
    while True:
        display_category_menu()
        choice = input("Pilih menu kategori: ")

        # Kembali ke menu utama
        if choice == "5":
            return client_socket

        try:
            if choice == "1":
                show_categories(client_socket)

            elif choice == "2":
                add_category(client_socket)

            elif choice == "3":
                edit_category(client_socket)

            elif choice == "4":
                delete_category(client_socket)

            else:
                print("\nPilihan tidak valid.")

        except ConnectionError:
            print("\nServer terputus.")

            # Reconnect
            client_socket = connect_with_retry()

def system_loop(client_socket):
    while True:
        display_system_menu()
        choice = input("Pilih menu sistem: ")

        # Kembali ke menu utama
        if choice == "3":
            return client_socket

        try:
            if choice == "1":
                check_server_health(client_socket)

            elif choice == "2":
                show_access_logs(client_socket)

            else:
                print("\nPilihan tidak valid.")

        except ConnectionError:
            print("\nServer terputus.")

            # Reconnect
            client_socket = connect_with_retry()

def connect_with_retry():
    while True:
        print("\n====================================")
        print("       CONNECTING TO SERVER")
        print("====================================")
        print("Server :", SERVER_HOST)
        print("Port   :", SERVER_PORT)

        try:
            client_socket = connect_to_server()

            print("\nConnected to server!")

            return client_socket

        except ConnectionRefusedError:
            print("\nGagal terhubung ke server.")
            print("Pastikan server.py sedang berjalan.")

        except socket.timeout:
            print("\nKoneksi ke server timeout.")

        except OSError as error:
            print("\nConnection error:", error)

        print("\n====================================")
        print("         CONNECTION FAILED")
        print("====================================")
        print("1. Reconnect to server")
        print("2. Quit")
        print("====================================")

        choice = input("Pilih opsi: ")

        if choice == "1":
            print("\nMencoba reconnect...")

        elif choice == "2":
            print("\nClient ditutup.")
            raise SystemExit

        else:
            print("\nPilihan tidak valid.")

def main():
    hostname, ip_address = get_client_identity()

    print("\n====================================")
    print("      STORAGE MANAGEMENT CLIENT")
    print("====================================")
    print("Hostname :", hostname)
    print("IP       :", ip_address)

    print("\nConnecting to server...")
    print("Server   :", SERVER_HOST, ":", SERVER_PORT)

    client_socket = connect_with_retry()
    if client_socket is None:
        return

    while True:
        display_main_menu()
        choice = input("Pilih menu utama: ")

        if choice == "1":
            client_socket = item_loop(client_socket)

        elif choice == "2":
            client_socket = rack_loop(client_socket)

        elif choice == "3":
            client_socket = category_loop(client_socket)

        elif choice == "4":
            client_socket = system_loop(client_socket)

        elif choice == "5":
            print("\nDisconnecting...")

            try:
                client_socket.close()
            except Exception:
                pass

            print("Client ditutup.")
            break

        else:
            print("\nPilihan tidak valid.")


if __name__ == "__main__":
    main()