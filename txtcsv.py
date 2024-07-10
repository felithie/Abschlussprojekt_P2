import csv
#Funktionen zum Konvertieren von TXT-Dateien in CSV-Dateien
def convert_txt_to_csv(txt_file_path, csv_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        for line in lines:
            
            row = line.strip().split()
            csv_writer.writerow(row)

# Beispiel verwenden
convert_txt_to_csv('data/ekg_data/05_Belastung.txt', 'data/csv_data/05_Belastung.csv')

#hat nicht so funktioniert wie wir uns das vorgestellt haben, Daten können nicht so gelesen werden wie aus der TXT-Datei