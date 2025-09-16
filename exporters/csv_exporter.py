import csv

def export_to_csv(matriks, nama_file):
    with open(nama_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in matriks.data:
            writer.writerow(row)
    print(f"Matriks berhasil diekspor ke {nama_file}")
