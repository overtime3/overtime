from CSV_Handler import CSV_Handler
from Json import Json, DisplayJson
from helpers.Constant import Constant
import collections

# Extra all the stop points or stations for each given line
class Extract_Stop_Points():
    csv_handler = CSV_Handler()
    csv_line_handler = CSV_Handler(Constant.DATASET_LINE_DIR)
    tube_transportation_line = csv_handler.get_single_field_from_csv("tfl_tube_mode.csv", "id")
    worker = DisplayJson(Constant.DATASET_LINE_DIR)

    for line in tube_transportation_line:
        worker.read_json_file(f"{line}_line_stop_points.json")
        line_json = worker.get_readable_json()

        total_tube = 0
        # Check if all of the stop points within each entry contains the tube mode, hence it is underground
        # We do not want stop points that is available on for buses
        for i, stop_point in enumerate(line_json):
            if "tube" in stop_point["modes"]:
                total_tube += 1
        accuracy = (total_tube/len(line_json)) * 100
        print(f'The accuracy for {line} is {accuracy}%')

        if int(accuracy) == 100:
            csv_line_handler.create_csv_file(line_json, f'{line}_stop_points.csv', "id", "commonName", "stopType", "lat", "lon")

extract = Extract_Stop_Points()

# Get all the tube lines such as jubilee, northern, victoria...
# def get_all_tube_lines():
#     csv_reader = CSV_Handler()
#     return csv_reader.get_single_field_from_csv("tfl_tube_mode.csv", "id")

# def get_all_stop_points(lines):
#     csv_reader = CSV_Handler(Constant.DATASET_LINE_DIR)
#     stop_points_by_line = collections.defaultdict(list)

#     for line in lines:
#         df = csv.get_multiple_field_from_csv(f'{line}_stop_points.csv', "id", "commonName", "lat", "lon")
#         print(Constant.LINE)
#         print(line)
#         print(df)

# csv = CSV_Handler(Constant.DATASET_LINE_DIR)
# df = csv.get_multiple_field_from_csv("victoria_stop_points.csv", "id", "commonName", "lat", "lon")

# get_all_stop_points(get_all_tube_lines())