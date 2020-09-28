
from os import path as ospath
import csv
import datetime
from time import sleep
import re
from overtime.inputs.rest import TflClient



class Input:
    """
        Base input handler class.
        
        Object Propertie(s):
        --------------------
        data : Dict
            A dictionary to hold all the node & edge information.

        See also:
        ---------
            CsvInput
            TflInput
    """

    def __init__(self):
        self.data = {}
        self.data['nodes'] = {}
        self.data['edges'] = {}



class CsvInput(Input):
    """
        A csv input handler for converting csv data into the standard data structure for graph creation.

        Parameter(s):
        -------------
        path : String
            The path of a csv file, for example '/data/network.csv'.
        
        Object Propertie(s):
        --------------------
        data : Dict
            Inherited from Input.
        path : String
            The path of the csv file.

        Example(s):
        -----------
            data = CsvInput('./network.csv')

        See also:
        ---------
            Input
            TflInput
    """

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.read()


    def read(self):
        # open the csv file at the specified path.
        with open(self.path, newline='') as csvfile:
            reader = csv.DictReader(csvfile) # initialize the csv reader.
            data = self.data
            ne = 0
            # for each row in the csv.
            for row in reader:
                # skip blank rows.
                if any(x.strip() for x in row):
                    # add edge data, conforming to data naming convention.
                    data['edges'][ne] = {
                        'node1': row['node1'],
                        'node2': row['node2'],
                        'tstart': row['tstart'],
                        'tend': None
                    }
                    # if 'tend' is specified in the csv, add it to data (default: None).
                    if 'tend' in row:
                        data['edges'][ne]['tend'] = row['tend']
                    ne += 1



class TflInput(Input):
    """
        An input handler that generates network data through the TflClient.

        Parameter(s):
        -------------
        lines : List
            A list of valid names (String) of lines on the TFL network.
            For example, ['bakerloo', 'central'].
        directions : List
            A list of valid directions (String) of routes on the line.
            For example, ['inbound', 'outbound'].
        times: List
            A list of valid 24hr times (String).
            For example, ['15:00', '15:15'].

        Object Propertie(s):
        --------------------
        data : Dict
            Inherited from Input.
        api : TflClient
            An instance of TflClient to be used for api requests.
        lines : List
            A list of valid names (String) of lines on the TFL network.
        directions : List
            A list of valid directions (String) of routes on the line.
        times : List
            A list of valid 24hr times (String).
        jpath : String
            The default path of the journeys csv file written once data is generated.
        spath : String
            The default path of the stations csv file written once data is generated.

        Example(s):
        -----------
            data = CsvInput('./network.csv')

        See also:
        ---------
            Input
            CsvInput
    """

    def __init__(self, lines=['bakerloo'], directions=['inbound', 'outbound'], times=['1400']):
        super().__init__()
        self.api = TflClient()
        self.lines = lines
        self.directions = directions
        self.times = times
        self.jpath = 'data/' + "_".join(lines) + "-" + "_".join(directions) + '.csv'
        self.spath = 'data/' + "_".join(lines) + '-stations' + '.csv'

        # check if the journeys csv path provided already exists.
        if not ospath.exists(self.jpath):
            for line in lines:
                for direction in directions:
                    # get the route information from the line and direction.
                    line_stations = self.get_line_routes(line, direction)
                    for time in times:
                        self.generate(line, direction, line_stations, time)
        else:
            print("{} already exists.".format(self.jpath))


    def generate(self, line_name, direction, line_stations, time):
        """
            A method of TflInput.
            Parameter(s):
            -------------
            line_name : String
                Valid name of a TFL line, such as 'bakerloo'.
            direction : String
                'inbound' or 'outbound'
            line_stations : Dict
                A dictionary of stations on the route of a line.
            time : String
                Valid 24hr time, such as '14:00'.
            
            Returns:
            --------
                None, writes two csv outputs.
                - Stations (nodes) csv.
                - Journeys (edges) csv.
        """
        # for each route on the specified lines.
        for name, stations in line_stations.items():
            print('\n<<< {} ({}), {} @ {} >>>\n'.format(name, line_name, direction, time))
            current_time = time # initialize current time at specified time.
            # for each station on the route (ordered sequence along line).
            for n in range(0, len(stations)):
                # attempt to get journeys at the current time between stations along the route.
                try:
                    # make the api request.
                    journey = self.get_journey(stations[n], stations[n+1], current_time)
                    # if no journey returned, skip it.
                    if not journey:
                        print('No available journey.')
                        continue
                    # if the returned journey is 'walking', skip it.
                    if 'Walk' in journey['name']:
                        print('No available line from {} to {} ({}).'.format(journey['departurePoint'], journey['arrivalPoint'], journey['name']))
                        continue
                    print('{} ---> {}, {} ({} mins @ {} >>> {})'.format(
                        journey['departurePoint'], journey['arrivalPoint'], journey['name'], journey['duration'],
                        self.update_time(journey['startDateTime']), self.update_time(journey['arrivalDateTime'])
                    ))
                    # update the current time to be the arrival time of the current journey.
                    current_time = self.update_time(journey['arrivalDateTime'])
                    # add the journey to the data.
                    self.add_journey(
                        journey['departurePoint'],
                        journey['arrivalPoint'],
                        self.convert_time(self.update_time(journey['startDateTime'])),
                        self.convert_time(self.update_time(journey['arrivalDateTime'])),
                        journey['name'],
                        direction,
                        current_time
                    )
                    # add the respective stations to the data.
                    self.add_station(journey['departurePoint'], stations[n], journey['departurePointLocation'][0], journey['departurePointLocation'][1])
                    self.add_station(journey['arrivalPoint'], stations[n+1], journey['arrivalPointLocation'][0], journey['arrivalPointLocation'][1])
                except IndexError:
                    break
            # once an entire route is processed, write the data to the csv files (each route is appended).
            self.write_stations_csv()
            self.write_journeys_csv()


    def get_line_routes(self, line, direction):
        """
            A method of TflInput.
            Parameter(s):
            -------------
            line : String
                Valid name of a TFL line, such as 'bakerloo'.
            direction : String
                'inbound' or 'outbound'
            
            Returns:
            --------
            rdata : Dict
                A dictionary with ordered sequence of stations for each route on the line.    
        """
        flag = False
        try:
            # make the api request.
            response = self.api.get_line_sequence(line, direction)
            rdata = {}
            # for each route in the response, add the list of ordered stations for that route into the dictionary.
            for route in response['orderedLineRoutes']:
                rdata[route['name']] = route['naptanIds']
        except KeyError:
            print("Key Error: response returned invalid data, client will request again in 5 seconds.")
            print(response)
            flag = True
        if flag:
            return self.get_line_routes(line, direction)
        return rdata


    def get_journey(self, origin, destination, time, sleep_time=0):
        """
            A method of TflInput.
            Parameter(s):
            -------------
            origin : String
                Valid naptanId of a TFL station, such as '940GZZLUPAC'.
            destination : String
                Valid naptanId of a TFL station, such as '940GZZLUPAC'.
            time : String
                Valid 24hr time, such as '14:00'.
            
            Returns:
            --------
            jdata[0] : Dict
                A dictionary with information about the journey returned from origin to destination with departing time 'time'.
        """
        # make the api request.
        response = self.api.get_journey(origin, destination, time.replace(':', ''), sleep_time=sleep_time)
        jdata = {}
        flag = False
        try:
            n = 0
            # for each journey option returned.
            for journey in response['journeys']:
                # for each leg of the journey (generally only ever one).
                for leg in journey['legs']:
                    # if the selected journey is earlier than the time specified, skip it.
                    if self.convert_time(self.update_time(journey['startDateTime'])) >= self.convert_time(time):
                        # filter the journey json for any required/useful information.
                        departure_name = leg['departurePoint']['commonName'].replace(' Underground Station', '')
                        arrival_name = leg['arrivalPoint']['commonName'].replace(' Underground Station', '')
                        jdata[n] = {
                            'startDateTime': journey['startDateTime'], # departure time
                            'arrivalDateTime': journey['arrivalDateTime'], # arrival time
                            'name': leg['instruction']['summary'], # journey name
                            'departurePoint': departure_name, # departure station name
                            'arrivalPoint': arrival_name, # arrival station name
                            'duration': leg['duration'], # journey duration
                            'departurePointLocation': (leg['departurePoint']['lat'], leg['departurePoint']['lon']), # departure geolocation
                            'arrivalPointLocation': (leg['arrivalPoint']['lat'], leg['arrivalPoint']['lon']) # arrival geolocation
                        }
                        n += 1
        except KeyError:
            print("Key Error: response returned invalid data, client will request again in 5 seconds.")
            print(response)
            flag = True
        if flag:
            return self.get_journey(origin, destination, time, sleep_time=5)
        if not jdata:
            print(jdata)
            print(response)
        return jdata[0]


    def add_station(self, label, naptan_id, lat, lon):
        """
            A method of TflInput.
            Parameter(s):
            -------------
            label : String
                The station's name.
            naptan_id : String
                The station's naptanId, such as '940GZZLUPAC'.
            lat : String
                The station's latitude.
            lon : String
                The station's longitude.
            
            Returns:
            --------
                None, updates data dictionary under 'nodes'.
        """
        self.data['nodes'][label] = {
                'label': label,
                'id': naptan_id,
                'lat': lat,
                'lon': lon
        }


    def add_journey(self, node1, node2, tstart, tend, line, direction, time):
        """
            A method of TflInput.
            Parameter(s):
            -------------
            node1 : String
                The departure station's name.
            node2 : String
                The arrival station's name.
            tstart : Integer
                The departure time in minutes from '0000'.
            tend : Integer
                The arrival time in minutes from '0000'.
            line : String
                A description of the journey.
            Direction : String
                The direction of the journey, either 'inbound' or 'outbound'.
            time : String
                The original time at which the journey was requested, for example '1305'.
            
            Returns:
            --------
                None, updates data dictionary under 'edges'.
        """
        self.data['edges']["-".join([line, direction, str(time)])] = {
            'node1': node1,
            'node2': node2,
            'tstart': tstart,
            'tend': tend,
            'line': line,
        }


    def update_time(self, time):
        """
            A method of TflInput.
            Parameter(s):
            -------------
            time : String
                Valid TFL response datetime, such as '17-08-20T14:05:10'.
            
            Returns:
            --------
            time : String
                Valid 24hr time, such as '1405', rounded to minutes.
        """
        # split time string into list with delimiters 'T', '-' and ':'.
        time = [int(i) for i in re.split('T|-|:', time)]
        # create corresponding datetime object.
        time = datetime.datetime(time[0], time[1], time[2], time[3], time[4])
        # create datetime delta of one minute.
        ### delta = datetime.timedelta(minutes=duration)
        # subtract one minute delta from original time.
        ### time = time + delta
        # return updated time in hours, minutes format.
        return ":".join(str(time).split(' ')[-1].split(':')[0:2])


    def convert_time(self, time):
        """
            A method of TflInput.
            Parameter(s):
            -------------
            time : String
                Valid 24hr time, such as '1405'.
            
            Returns:
            --------
            time : Integer
                A integer representing the number of minutes passed from '0000'.
        """
        time = time.split(':')[0:2]
        hours = int(time[0])
        minutes = int(time[1])
        return minutes + hours * 60


    def write_journeys_csv(self):
        """
            A method of TflInput.
            
            Returns:
            --------
                None, writes to journeys csv.
        """
        cols = ['node1', 'node2', 'tstart', 'tend', 'line'] # csv header
        try:
            with open(self.jpath, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cols) # initialize csv writer.
                writer.writeheader()
                # for each edge (journey) in data.
                for key, data in self.data['edges'].items():
                    writer.writerow(data) # write the edge to the row.

        except IOError:
            print("I/O Error; error writing to csv.")


    def write_stations_csv(self):
        """
            A method of TflInput.
            
            Returns:
            --------
                None, writes to stations csv.
        """
        cols = ['label', 'id', 'lat', 'lon'] # csv header
        try:
            with open(self.spath, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cols) # initialize csv writer.
                writer.writeheader()
                # for each node (station) in data.
                for key, data in self.data['nodes'].items():
                    writer.writerow(data) # write the node to the row.

        except IOError:
            print("I/O Error; error writing to csv.")
