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

    from services.process_request import show_items
    items = show_items(client_socket)

    item_id = input("\nID barang yang ingin diupdate: ")
    if not item_id:
        return
        
    try:
        item_id = int(item_id)
    except ValueError:
        print("ID barang harus berupa angka.")
        return
        
    # Find existing item
    old_item = None
    for item in items:
        # handle list/dict format just in case
        if isinstance(item, (list, tuple)):
            if item[0] == item_id:
                old_item = {"name": item[1], "stock": item[2]}
                if len(item) > 4:
                    old_item["rack_id"] = item[3]
                    old_item["category_id"] = item[4]
                break
        else:
            if item.get("id") == item_id:
                old_item = {
                    "name": item.get("name"), 
                    "stock": item.get("stock"),
                    "rack_id": item.get("rack_id"),
                    "category_id": item.get("category_id")
                }
                break

    if not old_item:
        print(f"Barang dengan ID {item_id} tidak ditemukan.")
        return

    if not _show_category_and_rack(client_socket):
        return

    print("Catatan: Biarkan kosong (tekan Enter) jika tidak ingin mengubah data.")

    name = input(f"Nama barang [{old_item['name']}]: ")
    if not name:
        name = old_item["name"]
        
    stock = input(f"Stock baru [{old_item['stock']}]: ")
    if not stock:
        stock = old_item["stock"]

    cat_label = old_item.get("category_id") if old_item.get("category_id") is not None else "Wajib diisi"
    category_id = input(f"ID kategori [{cat_label}]: ")
    if not category_id and old_item.get("category_id") is not None:
        category_id = old_item.get("category_id")

    rack_label = old_item.get("rack_id") if old_item.get("rack_id") is not None else "Wajib diisi"
    rack_id = input(f"ID rak [{rack_label}]: ")
    if not rack_id and old_item.get("rack_id") is not None:
        rack_id = old_item.get("rack_id")

    # If the user still leaves it blank when it's Mandatory (no old data to fallback to)
    if not category_id or not rack_id:
        print("Kategori dan Rak wajib diisi jika data sebelumnya tidak tersedia.")
        return

    try:
        stock = int(stock)
        category_id = int(category_id)
        rack_id = int(rack_id)
    except ValueError:
        print("Stock, ID kategori, dan ID rak harus berupa angka.")
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

    from services.process_request import show_items
    show_items(client_socket)

    item_id = input("\nID barang yang akan dihapus: ")

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
        print("Pesan:", response.get("messages", "Barang berhasil dihapus."))
    else:
        print("\nGagal:", response.get("messages", "Terjadi kesalahan"))

