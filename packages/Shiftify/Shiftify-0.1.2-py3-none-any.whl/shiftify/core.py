import csv
import json

class Convert:
    def __init__(self, delimiter=',', quotechar='"'):
        self.delimiter = delimiter
        self.quotechar = quotechar

    def csv_to_json(self, csv_file_path, json_file_path):
        try:
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=self.delimiter, quotechar=self.quotechar)
                data = [row for row in reader]
            with open(json_file_path, mode='w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=4)
        except Exception as e:
            print(f"An error occurred: {e}")

    def json_to_csv(self, json_file_path, csv_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                # Automatically detect fieldnames from the first item's keys
                if data:
                    fieldnames = data[0].keys()
                else:
                    raise ValueError("JSON file is empty or data is not in expected format")

            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=self.delimiter, quotechar=self.quotechar)
                writer.writeheader()
                for item in data:
                    writer.writerow(item)
        except Exception as e:
            print(f"An error occurred: {e}")