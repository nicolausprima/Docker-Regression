import json

def export_to_json(matriks, nama_file):
    data_json = {
        "matrix_data": matriks.data,
        "rows": len(matriks.data),
        "columns": len(matriks.data[0]) if matriks.data else 0
    }
    with open(nama_file, 'w', encoding='utf-8') as file:
        json.dump(data_json, file, indent=2)
    print(f"Matriks berhasil diekspor ke {nama_file}")
