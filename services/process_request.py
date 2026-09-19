def show_items(client_socket):
    print("\n=== DAFTAR BARANG ===")

    response = send_request(
        client_socket,
        "GET_ITEMS",
        {}
    )

    if response["status"] == "OK":

        items = response["data"]

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
        print("Gagal:", response["message"])
