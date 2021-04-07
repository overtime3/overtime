from abc import ABC, abstractmethod
import json 
from helpers.Constant import Constant
from Json import Json, DisplayJson

class TFL_Default(ABC):
    def __init__(self, dataset_path=Constant.DATASET_DIR):
        self.dataset_path = dataset_path

    def response_status_code(self, status_code: int, url: str, throws_exception: True):
        print(f'Fetching from {url}')
        if status_code != 200:
            if throws_exception:
                raise Exception(status_code)
            else:
                print(f'Response: {status_code}, (exception disabled)')
        else:
            print(f'Response: {status_code}')
        
    # Save the dataset with a specific name and under specific file path
    def save_as_json(self, dataset, file_name: str, dataset_path: str):
        json = Json(dataset_path)
        json_file_path = json.create_json_file(dataset, file_name)
        return json_file_path

    # Remove space from string, we do not want space in file names
    def replace_space_by_delimiter(self, string: str) -> str:
        return "".join([Constant.FILE_NAME_DELIMITER if string[i].isspace() else string[i] for i in range(len(string))])

    # Main interface method to get and save certain TFL data 
    @abstractmethod
    def get_and_save_tfl_dataset(self):
        pass