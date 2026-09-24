from tabulate import tabulate
from client.connection import send_request

def show_categories(client_socket):
    print("\n=== DAFTAR KATEGORI ===")
    response = send_request(client_socket, "GET_CATEGORY", {})
    if response.get("status") is True:
        categories = response.get("datas") or []
        if not categories:
            print("Tidak ada data kategori.")
            return []

        table = []
        for cat in categories:
            table.append([cat.get("id"), cat.get("name")])

        print(tabulate(table, headers=["ID Kategori", "Nama Kategori"], tablefmt="grid"))
        return categories
    else:
        print("Gagal:", response.get("messages", "Terjadi kesalahan"))
        return []

def add_category(client_socket):
    print("\n=== TAMBAH KATEGORI ===")
    name = input("Nama Kategori: ")
    if not name:
        print("Nama kategori tidak boleh kosong.")
        return

    payload = {"name": name}
    response = send_request(client_socket, "ADD_CATEGORY", payload)

    if response.get("status") is True:
        print("\nKategori berhasil ditambahkan.")
    else:
        print("\nGagal:", response.get("messages", "Terjadi kesalahan"))

def edit_category(client_socket):
    print("\n=== EDIT KATEGORI ===")
    print("Catatan: Biarkan kosong (tekan Enter) jika tidak ingin mengubah data tertentu.")
    categories = show_categories(client_socket)
    
    category_id = input("\nID kategori yang ingin diedit: ")
    if not category_id:
        return
        
    try:
        category_id = int(category_id)
    except ValueError:
        print("ID kategori harus berupa angka.")
        return

    # Find existing category
    old_category = None
    for cat in categories:
        if cat.get("id") == category_id:
            old_category = cat
            break
            
    if not old_category:
        print(f"Kategori dengan ID {category_id} tidak ditemukan.")
        return

    name = input(f"Nama Kategori Baru [{old_category.get('name')}]: ")
    if not name:
        name = old_category.get("name")

    payload = {"category_id": category_id, "name": name}
    response = send_request(client_socket, "EDIT_CATEGORY", payload)

    if response.get("status") is True:
        print("\nKategori berhasil diupdate.")
    else:
        print("\nGagal:", response.get("messages", "Terjadi kesalahan"))

def delete_category(client_socket):
    print("\n=== HAPUS KATEGORI ===")

    category_id = input("ID kategori yang akan dihapus: ")

    try:
        category_id = int(category_id)
    except ValueError:
        print("ID kategori harus berupa angka.")
        return

    confirm = input(
        "Yakin ingin menghapus kategori ini? (y/n): "
    )

    if confirm.lower() != "y":
        print("Penghapusan kategori dibatalkan.")
        return

    payload = {
        "category_id": category_id
    }

    response = send_request(
        client_socket,
        "DELETE_CATEGORY",
        payload
    )

    if response.get("status") is True:
        print("\nKategori berhasil dihapus.")
        print("Pesan:", response.get("messages", "Operasi berhasil."))
    else:
        print("\nGagal menghapus kategori.")
        print("Pesan:", response.get("messages", "Terjadi kesalahan."))


