import json, requests, time
from helpers.Constant import Constant
from CSV_Handler import CSV_Handler
from TFL_Default import TFL_Default

class TFL_Stop_Point_Timetable(TFL_Default):
    def __init__(self, dataset_path=Constant.DATASET_TIMETABLE_DIR):
        super().__init__(dataset_path)

    # params: line: the tube line such as Central or Circle 
    # stop_point_naptan_code: the id for the station e.g. 940GZZLUCW is Bank Underground Station
    # direction: value can be either inbound or outbound
    def get_stop_point_timetable(self, line: str, stop_point_naptan_code: str, direction: str):
        url = f'{Constant.ROOT_URL}/Line/{line}/Timetable/{stop_point_naptan_code}?direction={direction}&key={Constant.API_KEY}'
        response = requests.get(url)        # This get request can take up to a minute! Lots of data
        self.response_status_code(status_code=response.status_code, url=url, throws_exception=False)
        print(f'Response time: {response.elapsed.total_seconds()} seconds')
        dataset = response.json()
        return dataset
    
    # API request and save the response to JSON
    def get_and_save_tfl_dataset(self, line: str, station_name: str, stop_point_naptan_code: str, direction: str):
        station_name = self.replace_space_by_delimiter(station_name) # Replace space with file delimiter
        file_name = f'{station_name}_{line}_{direction}_timetable.json'
        dataset = self.get_stop_point_timetable(line, stop_point_naptan_code, direction)
        file_path = self.save_as_json(dataset, file_name, f'{self.dataset_path}{line.lower()}/')
        return file_path

    # Get all the stop points timetable under all the given transportation line
    def get_and_save_multiple_tfl_dataset(self, lines):
        csv_handler = CSV_Handler(Constant.DATASET_LINE_DIR)

        for line in lines:
            if line != "central" or line != "circle" or line != "district":
                file_name = line + "_stop_points.csv"
                df = csv_handler.get_multiple_field_from_csv(file_name, "id", "commonName")
                request_tracker = 0
                print("")
                print(Constant.LINE)
                for _, row in df.iterrows():
                    if request_tracker == 12:
                        print("Sleeping")
                        time.sleep(20)  # Prevent us calling too many request and triggering 429 status code
                        request_tracker = 0
                    self.get_and_save_tfl_dataset(line, row['commonName'], row['id'], "inbound")
                    self.get_and_save_tfl_dataset(line, row['commonName'], row['id'], "outbound")
                    request_tracker+=1 


if __name__ == "__main__":
    # 940GZZLUBNK
    timetable = TFL_Stop_Point_Timetable()
    # json_file_path = timetable.get_and_save_tfl_dataset('central', "Bank Underground Station", "940GZZLUBNK", "outbound")

    
    csv = CSV_Handler()
    tube_lines = csv.get_single_field_from_csv('tfl_tube_mode.csv', "id") # Get all tube lines such as central, piccadilly, victoria...
    timetable.get_and_save_multiple_tfl_dataset(tube_lines)
