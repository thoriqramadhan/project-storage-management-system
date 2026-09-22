from tabulate import tabulate

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
            return []

        table = []

        for item in items:
            # Server returns: id, name, stock, rack_id, category_id, category_name, rack_name, updated_at
            cat_name = "-"
            rack_name = "-"
            
            if isinstance(item, dict):
                cat_name = item.get("category_name", item.get("category_id", "-"))
                rack_name = item.get("rack_name", item.get("rack_id", "-"))
            elif len(item) > 6:
                cat_name = item[5] if item[5] is not None else "-"
                rack_name = item[6] if item[6] is not None else "-"

            table.append([
                item.get("id") if isinstance(item, dict) else item[0],
                item.get("name") if isinstance(item, dict) else item[1],
                cat_name,
                rack_name,
                item.get("stock") if isinstance(item, dict) else item[2]
            ])

        print(
            tabulate(
                table,
                headers=[
                    "ID",
                    "Barang",
                    "Kategori",
                    "Rak",
                    "Stock"
                ],
                tablefmt="grid"
            )
        )
        return items

    else:
        print("Gagal:", response["messages"])
        return []
