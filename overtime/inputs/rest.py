
import requests as reqs
from time import sleep



class Client:
    """
        Rest API client base class.

        Parameter(s):
        -------------
        base_url : String
            The root url of the REST api.

        Object Propertie(s):
        --------------------
        base : String
            The root url of the REST api.

        Example(s):
        -----------
            api_handler = Client('https://dog.ceo/api/')

        See also:
        ---------
            TflClient
    """

    def __init__(self, base_url):
        self.base = str(base_url)


    def get(self, url, query=''):
        """
            A method of TflClient.
            Parameter(s):
            -------------
            url : String
                Extended request url, for example 'breeds/list/all'
            query : String
                Any additional query parameters to be included.
            
            Returns:
            --------
                A json response from the specified url.
        """
        return reqs.get(self.base + url + query).json()



class TflClient(Client):
    """
        Rest API client for the TFL (Transport for London) api service.

        Object Propertie(s):
        --------------------
        base : String
            Inherited from Client.

        Example(s):
        -----------
            tfl_api_handler = TflClient()

        See also:
        ---------
            Client
    """

    def __init__(self):
        super().__init__('https://api.tfl.gov.uk/')


    def get_line(self, name):
        """
            A method of TflClient.
            Parameter(s):
            -------------
            name : String
                Valid name of a TFL line, such as 'bakerloo'.
            
            Returns:
            --------
                A json response with details about the specified line.
        """
        return reqs.get(self.base + 'Line/' + name + '/Route/').json()


    def get_station_by_name(self, name):
        """
            A method of TflClient.
            Parameter(s):
            -------------
            name : String
                Valid name of a TFL station, such as 'Oxford Circus'.
            
            Returns:
            --------
                A json response with details about the specified station.
        """
        return reqs.get(self.base + 'StopPoint/Search/' + name).json()['matches'][0]


    def get_line_stations(self, line):
        """
            A method of TflClient.
            Parameter(s):
            -------------
            line : String
                Valid name of a TFL line, such as 'bakerloo'.
            
            Returns:
            --------
                A json response with details about the specified line's stations.
        """
        return reqs.get(self.base + 'Line/' + line + '/StopPoints').json()


    def get_line_sequence(self, line, direction):
        """
            A method of TflClient.
            Parameter(s):
            -------------
            line : String
                Valid name of a TFL line, such as 'bakerloo'.
            direction : String
                'inbound' or 'outbound'
            
            Returns:
            --------
                A json response with details about the specified line's stations, along a particular set of route(s).
                Note: one line can have a number of routes associated with it.
        """
        return reqs.get(self.base + 'Line/' + line + '/Route/Sequence/' + direction).json()


    def get_journey(self, from_id, to_id, time, timel='departing', sleep_time=0.5):
        """
            A method of TflClient.
            Parameter(s):
            -------------
            from_id : String
                Valid naptanId of a TFL station, such as '940GZZLUPAC'.
            to_id : String
                Valid naptanId of a TFL station, such as '940GZZLUPAC'.
            time : String
                Valid 24hr time, such as '1400'.
            timel : String
                'departing' (recommended) or 'arriving'.
            
            Returns:
            --------
                A json response with details about the journey found between the specified stations.
                Note: multiple journeys are returned as options.
        """
        sleep(sleep_time) # limit query speed to reduce chance of api timeout (this function gets called alot).
        return reqs.get(
            self.base + '/Journey/JourneyResults/' + from_id + '/to/' + to_id
            + '?mode=tube' # only use tube (when possible)
            + '&useMultiModalCall=false' # don't return multiple journey options for different modes of transport
            + '&routeBetweenEntrances=false' # only return journeys between stations.
            + '&journeypreference=leastwalking' # prefer journeys that take the least time.
            + '&time=' + time # search for next available journeys after 'time'.
            + '&timel=' + timel # time is either 'departing' or 'arrival'.
        ).json()
