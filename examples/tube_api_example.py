
from inputs.rest import TflClient

api = TflClient()

station = api.get_station_by_name('victoria')
print(station)


line_stations = api.get_line_stations('victoria')

print('VICTORIA:')
api.get_line_sequence('victoria', 'inbound')

#print('CENTRAL:')
#api.get_line_sequence('central', 'inbound')

# timetable = api.get_timetable('victoria', 'HUBWHC', 'HUBBRX')
# print(timetable)
# for station in timetable['stations']:
#     print(station['name'])

response = api.get_journey('1000248', '1000173', '1400')
print(response)

for items in response:
    print(items)

for journey in response['journeys']:
    print('NEW JOURNEY!!!')
    for leg in journey['legs']:
        print(leg['departurePoint']['commonName'])
        print(leg['arrivalPoint']['commonName'])
        print(leg['duration'])
        print(leg)


station1 = api.get_station_by_name('TottenhamHale')
station2 = api.get_station_by_name('Brixton')


response = api.get_journey(station1['icsId'], station2['icsId'], '1400')
for journey in response['journeys']:
    print('NEW JOURNEY!!!')
    for leg in journey['legs']:
        print(leg['departurePoint']['commonName'])
        print(leg['arrivalPoint']['commonName'])
        print(leg['duration'])
        for station in leg['path']['stopPoints']:
            print(station['name'])

for journey in response['journeys']:
    print('NEW JOURNEY!!!')
    print(journey)
    for item in journey:
        print(item)
    for leg in journey['legs']:
        for item in leg:
            print(item)
        for path in leg['path']:
            print(path)


victoria = api.get_line('victoria')
for route in victoria['routeSections']:
    print(route['name'])
    print(route['direction'])
    print(route['originator'], route['destination'])
