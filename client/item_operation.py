from tabulate import tabulate
from client.connection import send_request

def _show_category_and_rack(client_socket):
    print("\nMengambil data Kategori dan Rak...")
    cat_res = send_request(client_socket, "GET_CATEGORY", {})
    if cat_res.get("status") is not True:
        print("Gagal mengambil data kategori:", cat_res.get("messages", "Error"))
        return False
        
    rack_res = send_request(client_socket, "GET_RACK", {})
    if rack_res.get("status") is not True:
        print("Gagal mengambil data rak:", rack_res.get("messages", "Error"))
        return False
        
    categories = cat_res.get("datas") or []
    racks = rack_res.get("datas") or []
    
    print("\n[ Kategori Tersedia ]")
    cat_table = [[c.get("id"), c.get("name")] for c in categories]
    print(tabulate(cat_table, headers=["ID Kategori", "Nama Kategori"], tablefmt="simple_grid"))

    print("\n[ Rak Tersedia ]")
    rack_table = [[r.get("id"), r.get("name")] for r in racks]
    print(tabulate(rack_table, headers=["ID Rak", "Nama Rak"], tablefmt="simple_grid"))
    print()
    return True
def add_item(client_socket):
    print("\n=== TAMBAH BARANG ===")
    
    if not _show_category_and_rack(client_socket):
        return

    name = input("Nama barang   : ")
    category_id = input("ID kategori   : ")
    rack_id = input("ID rak        : ")
    stock = input("Stock         : ")

    # Validasi input
    if not name:
        print("Nama barang tidak boleh kosong.")
        return

    try:
        category_id = int(category_id)
        rack_id = int(rack_id)
        stock = int(stock)
    except ValueError:
        print("ID kategori, ID rak, dan stock harus berupa angka.")
        return

    if stock < 0:
        print("Stock tidak boleh negatif.")
        return

    payload = {
        "name": name,
        "category_id": category_id,
        "rack_id": rack_id,
        "stock": stock,
    }

    response = send_request(
        client_socket,
        "ADD_ITEMS",
        payload
    )

    if response.get("status") is True:
        print("\nBarang berhasil ditambahkan.")
    else:
        print("\nGagal:", response.get("messages", "Terjadi kesalahan"))



def update_stock(client_socket):
    print("\n=== UPDATE STOCK ===")

    if not _show_category_and_rack(client_socket):
        return

    item_id = input("ID barang    : ")
    name = input("Nama barang  : ")
    stock = input("Stock baru   : ")
    category_id = input("ID kategori  : ")
    rack_id = input("ID rak       : ")

    try:
        item_id = int(item_id)
        stock = int(stock)
        category_id = int(category_id)
        rack_id = int(rack_id)
    except ValueError:
        print("Semua ID dan stock harus berupa angka.")
        return

    if stock < 0:
        print("Stock tidak boleh negatif.")
        return

    payload = {
        "item_id": item_id,
        "name": name,
        "stock": stock,
        "category_id": category_id,
        "rack_id": rack_id
    }

    response = send_request(
        client_socket,
        "UPDATE_STOCKS",
        payload
    )

    if response.get("status") is True:
        print("\nStock berhasil diperbarui.")
    else:
        print("\nGagal:", response.get("messages", "Terjadi kesalahan"))

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

    payload = {
        "item_id": item_id
    }

    response = send_request(
        client_socket,
        "DELETE_ITEMS",
        payload
    )

    if response.get("status") is True:
        print("\nBarang berhasil dihapus.")
    else:
        print("\nGagal:", response.get("messages", "Terjadi kesalahan"))

