import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

class Constant(object):
    # Sensitive Info
    API_KEY = settings.API_KEY

    # URL 
    ROOT_URL = "https://api.tfl.gov.uk"
    TRANSPORT_MODE = f'{ROOT_URL}/Line/Meta/Modes?{API_KEY}'

    # Directory Path
    DATASET_DIR = "api_dataset/"
    DATASET_LINE_DIR = DATASET_DIR + "line/"
    DATASET_TIMETABLE_DIR = DATASET_DIR + "timetable/"

    # Default line mode
    DEFAULT_MODE = "tube"

    # The London transportation network lines
    LINE_TYPE = ["bakerloo", "central", "circle", "district",
    "hammersmith & city", "jubilee", "metropolitan", "northern",
    "piccadilly", "victoria", "waterloo & city", "dlr", 
    "emirate air line cable car", "london overground"]

    # Json Files
    STATION_JSON_FILE_PATTERN = "_line_station.json"

    FILE_NAME_DELIMITER = "_"

    # Line break
    LINE = "=====" * 5