import tabulate

from client.connection import send_request

def show_items(client_socket):
    print("\n=== DAFTAR BARANG ===")

    response = send_request(
        client_socket,
        "CHECK_STOCKS",
        {}
    )

    if response["status"] is True:

        items = response["datas"]

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
        print("Gagal:", response["messages"])
