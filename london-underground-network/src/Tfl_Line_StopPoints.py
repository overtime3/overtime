import json, requests
from helpers.Constant import Constant
from TFL_Default import TFL_Default
from CSV_Handler import CSV_Handler
from Json import Json

import numpy as np

# Get information related to a given line. For example victoria line
class Tfl_Line_StopPoints(TFL_Default):
    def __init__(self):
        self.x = 2

    # Get all stations under a specific line
    # 
    def get_line_stations(self, line):
        url = f'{Constant.ROOT_URL}/Line/{line}/StopPoints?{Constant.API_KEY}'
        response = requests.get(url)
        self.response_status_code(response.status_code, url)
        dataset = response.json()
        return dataset
    
    def get_and_save_tfl_dataset(self, line, dataset_path=Constant.DATASET_LINE_DIR):
        file_name = f'{line}_line_stop_points.json'
        dataset = self.get_line_stations(line)
        file_path = self.save_as_json(dataset, file_name, dataset_path)
        return file_path


if __name__ == "__main__":
    csv = CSV_Handler()
    # Loads all the lines or service under the tube transport mode
    tfl_tube_line = csv.get_single_field_from_csv("tfl_tube_mode.csv", "id")

    line_station = Tfl_Line_StopPoints()

    # For each line call the TfL API to get stop points
    for line in tfl_tube_line:
        respond = line_station.get_and_save_tfl_dataset(line)


