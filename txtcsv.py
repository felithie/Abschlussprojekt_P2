import csv

def convert_txt_to_csv(txt_file_path, csv_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        for line in lines:
            # Assuming the values in TXT file are space-separated
            row = line.strip().split()
            csv_writer.writerow(row)

# Beispiel verwenden
convert_txt_to_csv('data/ekg_data/05_Belastung.txt', 'data/csv_data/05_Belastung.csv')
