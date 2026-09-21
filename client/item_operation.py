from client.connection import send_request

def add_item(client_socket):
    print("\n=== TAMBAH BARANG ===")

    name = input("Nama barang   : ")
    category_id = input("ID kategori   : ")
    rack_id = input("ID rak   : ")
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

    if response["status"] is True:
        print("\nBarang berhasil ditambahkan.")
    else:
        print("\nGagal:", response["message"])



def update_stock(client_socket):
    print("\n=== UPDATE STOCK ===")

    item_id = input("ID barang    : ")
    name = input("Nama barang  : ")
    stock = input("Stock baru   : ")
    category_id = input("ID kategori  : ")
    rack_id = input("ID rak      : ")

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

    if response["status"] is True:
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

    payload = {
        "item_id": item_id
    }

    response = send_request(
        client_socket,
        "DELETE_ITEMS",
        payload
    )

    if response["status"] is True:
        print("\nBarang berhasil dihapus.")
    else:
        print("\nGagal:", response["message"])

