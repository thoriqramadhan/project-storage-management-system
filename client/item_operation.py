from client.connection import send_request

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

