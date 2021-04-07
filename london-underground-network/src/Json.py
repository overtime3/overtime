import os, json, fnmatch
from helpers.Constant import Constant
from abc import ABCMeta, abstractmethod

class Json():
    def __init__(self, dataset_path=Constant.DATASET_DIR):
        self.dataset_path = dataset_path
        self.json_file_path = None
        self.readable_json = None
    
    def create_json_file(self, dataset, file_name: str):
        with open(os.path.join(self.dataset_path, file_name), 'w') as f:
            json.dump(dataset, f)
            return self.dataset_path + file_name

    def load_json_file(self, file_name: str):
        with open(f'{self.dataset_path}{file_name}', 'r') as json_file:
            data = json_file.read()
            return data

    def read_json_file(self, file_name: str):
        readable_json = json.loads(self.load_json_file(file_name))
        self.readable_json = readable_json
        return readable_json

    def get_readable_json(self):
        return self.readable_json

    @abstractmethod
    def get_json_file_names(self, regex_file: str):
        pass

class DisplayJson(Json):
    # Prol use mixin to call Json object :)
    def __init__(self, dataset_path=Constant.DATASET_DIR):
        super().__init__(dataset_path)
        
    def get_json_file_names(self, regex_file):
        file_names = []
        for f_name in os.listdir(Constant.DATASET_DIR):
            print(f_name)
            if fnmatch.fnmatch(f_name, regex_file):
                file_names.append(f'{Constant.DATASET_DIR}/{f_name}')
        return file_names

    def pretty_print_json(self, file, indent=4):
        parsed_data = self.load_json_file("tfl_tube_mode.json")
        print(json.dumps(parsed_data, indent=indent, sort_keys=True))

    def display_json(self, regex_file=f'*{Constant.STATION_JSON_FILE_PATTERN}'):
        json_file_names = self.get_json_file_names(regex_file)
        print(json_file_names)
        for file_name in json_file_names:
            self.pretty_print_json(file_name)

if __name__ == "__main__":
    pass
