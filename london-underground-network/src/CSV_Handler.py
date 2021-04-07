import csv, collections
import pandas as pd
from helpers.Constant import Constant

class CSV_Handler():
    def __init__(self, dataset_path=Constant.DATASET_DIR):
        self.dataset_path = dataset_path

    # Converts dataset to cvs, where *fields is the array of fields
    def create_csv_file(self, dataset, file_name: str, *fields):
        with open(f'{self.dataset_path}/{file_name}', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            for i in range(len(dataset)):
                data_row = []
                for field in fields:
                    data_row.append(dataset[i][field])
                writer.writerow(data_row)


    def get_single_field_from_csv(self, file_name: str, field: str):
        result = []
        with open(f'{self.dataset_path}/{file_name}', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line = 0
            for row in csv_reader:
                result.append(row[field]) if line != 0 else None
                line += 1
        return result
    
    # Converts selected fields from CSV - combine them and make dataframe
    def get_multiple_field_from_csv(self, file_name: str,  *fields):
        df = pd.read_csv(f'{self.dataset_path}/{file_name}')
        frames = []
        for field in fields:
            frames.append(df[field])
        result = pd.concat(frames, join="outer", axis=1)
        return result

    def display_csv(self, file_name: str):
        df = pd.read_csv(f'{self.dataset_path}/{file_name}')
        print(df.to_string())

h = CSV_Handler()
file_name = 'tfl_tube_mode.csv'
df = h.get_multiple_field_from_csv(file_name, "id", "name")
