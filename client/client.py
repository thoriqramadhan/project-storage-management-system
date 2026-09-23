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

from client.item_operation import add_item, update_stock, delete_item
from services.process_request import show_items
from client.rack_operation import show_racks, add_rack, edit_rack, delete_rack
from client.category_operation import show_categories, add_category, edit_category, delete_category
from client.health import check_server_health, show_access_logs

def item_loop(client_socket):
    while True:
        display_item_menu()
        choice = input("Pilih menu barang: ")
        if choice == "1":
            show_items(client_socket)
        elif choice == "2":
            add_item(client_socket)
        elif choice == "3":
            update_stock(client_socket)
        elif choice == "4":
            delete_item(client_socket)
        elif choice == "5":
            break
        else:
            print("\nPilihan tidak valid.")

def rack_loop(client_socket):
    while True:
        display_rack_menu()
        choice = input("Pilih menu rak: ")
        if choice == "1":
            show_racks(client_socket)
        elif choice == "2":
            add_rack(client_socket)
        elif choice == "3":
            edit_rack(client_socket)
        elif choice == "4":
            break
        else:
            print("\nPilihan tidak valid.")

def category_loop(client_socket):
    while True:
        display_category_menu()
        choice = input("Pilih menu kategori: ")
        if choice == "1":
            show_categories(client_socket)
        elif choice == "2":
            add_category(client_socket)
        elif choice == "3":
            edit_category(client_socket)
        elif choice == "4":
            break
        else:
            print("\nPilihan tidak valid.")

def system_loop(client_socket):
    while True:
        display_system_menu()
        choice = input("Pilih menu sistem: ")
        if choice == "1":
            check_server_health(client_socket)
        elif choice == "2":
            show_access_logs(client_socket)
        elif choice == "3":
            break
        else:
            print("\nPilihan tidak valid.")

def connect_with_retry():
    while True:
        print("\nConnecting to server...")
        print(
            "Server   :",
            SERVER_HOST,
            ":",
            SERVER_PORT
        )

        try:
            client_socket = connect_to_server()

            print("Connected to server!")

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
            return None

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
        try: 
            display_main_menu()
            choice = input("Pilih menu utama: ")

            if choice == "1":
                item_loop(client_socket)
            elif choice == "2":
                rack_loop(client_socket)
            elif choice == "3":
                category_loop(client_socket)
            elif choice == "4":
                system_loop(client_socket)
            elif choice == "5":
                print("\nDisconnecting...")
                client_socket.close()
                print("Client ditutup.")
                break
            else:
                print("\nPilihan tidak valid.")
        except:
            print(connect_with_retry())
if __name__ == "__main__":
    main()