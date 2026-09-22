from tabulate import tabulate
from client.connection import send_request

def show_racks(client_socket):
    print("\n=== DAFTAR RAK ===")
    response = send_request(client_socket, "GET_RACK", {})
    if response.get("status") is True:
        racks = response.get("datas") or []
        if not racks:
            print("Tidak ada data rak.")
            return []

        table = []
        for rack in racks:
            table.append([rack.get("id"), rack.get("name")])

        print(tabulate(table, headers=["ID Rak", "Nama Rak"], tablefmt="grid"))
        return racks
    else:
        print("Gagal:", response.get("messages", "Terjadi kesalahan"))
        return []

def add_rack(client_socket):
    print("\n=== TAMBAH RAK ===")
    name = input("Nama Rak: ")
    if not name:
        print("Nama rak tidak boleh kosong.")
        return

    payload = {"name": name}
    response = send_request(client_socket, "ADD_RACK", payload)

    if response.get("status") is True:
        print("\nRak berhasil ditambahkan.")
    else:
        print("\nGagal:", response.get("messages", "Terjadi kesalahan"))

def edit_rack(client_socket):
    print("\n=== EDIT RAK ===")
    print("Catatan: Biarkan kosong (tekan Enter) jika tidak ingin mengubah data tertentu.")
    racks = show_racks(client_socket)
    
    rack_id = input("\nID rak yang ingin diedit: ")
    if not rack_id:
        return
        
    try:
        rack_id = int(rack_id)
    except ValueError:
        print("ID rak harus berupa angka.")
        return

    # Find existing rack
    old_rack = None
    for rack in racks:
        if rack.get("id") == rack_id:
            old_rack = rack
            break
            
    if not old_rack:
        print(f"Rak dengan ID {rack_id} tidak ditemukan.")
        return

    name = input(f"Nama Rak Baru [{old_rack.get('name')}]: ")
    if not name:
        name = old_rack.get("name")

    payload = {"rack_id": rack_id, "name": name}
    response = send_request(client_socket, "EDIT_RACK", payload)

    if response.get("status") is True:
        print("\nRak berhasil diupdate.")
    else:
        print("\nGagal:", response.get("messages", "Terjadi kesalahan"))
