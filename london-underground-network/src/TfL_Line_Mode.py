import json, requests
from helpers.Constant import Constant
from CSV_Worker import CSV_Worker
from TFL_Default import TFL_Default
from Json import Json, DisplayJson

# Get all the TfL lines under a given transport mode i.e. tube
class TFL_Line_Mode(TFL_Default):
    def __init__(self, mode=Constant.DEFAULT_MODE):
        self.mode = mode

    # API request to TFL for all the lines given the transport mode
    # Return the API respond as JSOn
    def get_line_by_mode(self):
        url = f'{Constant.ROOT_URL}/Line/Mode/{self.mode}?{Constant.API_KEY}'
        response = requests.get(url)
        self.response_status_code(response.status_code, url)
        dataset = response.json()
        return dataset

    # API request and save respond to JSON
    def get_and_save_tfl_dataset(self, file_name, dataset_path=Constant.DATASET_DIR):
        dataset = self.get_line_by_mode()
        file_path = self.save_as_json(dataset, file_name, dataset_path)
        return file_path

if __name__ == "__main__":
    # Calls the Tfl API to get all the line under a given transportation mode i.e. tube will get central, dlr, piccadilly...
    # Save the API respond as JSON
    tfl_line_mode = TFL_Line_Mode()
    file_path = tfl_line_mode.get_and_save_tfl_dataset("tfl_tube_mode.json")

    # Loads the json file given the file path
    display = DisplayJson()
    result = display.read_json_file(file_path)

    # Converts the json of tfl tube mode to CSV with only the fields we want
    csv_writer = CSV_Worker()
    csv_writer.create_csv_file(result, "tfl_tube_mode.csv", "id", "name", "modeName")

