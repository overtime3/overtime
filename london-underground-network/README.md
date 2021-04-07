# London-Underground-Temporal-Network

This is the data mining part of the project. We will be using the TfL API to gather all the London Underground line timetable for all the stop points or stations.

This process involves different steps:
1. Data collections: Gather the data through the API, the API will return as a JSON format. I have created different multiple functions to gather different types of data. This will increase the scalability in case we want to gather other types of data in the future. Since we are Since we will be only developing the network for London Underground network. 
2. Featur extraction and data cleaning: We do not need all of the fields.


### TfL API 

The TfL API provides the latest up to date live data from the London transportation network.
To get access the API, you can access through https://api.tfl.gov.uk/. To use the API, you will need the API keys, which you can request by contacting the TfL developers or fill out the register on their website [source].

This is a new API url which is modern and contains good documentation: https://api-portal.tfl.gov.uk/apis.


### TfL Terms and Condition

The data will be used for educational purpose and will align with the terms and condition set out by TfL.

For full details: https://tfl.gov.uk/corporate/terms-and-conditions/transport-data-service


https://techforum.tfl.gov.uk/t/problems-with-line-timetable/1086

https://api-portal.tfl.gov.uk/api-details#api=Line&operation=Line_TimetableToByPathFromStopPointIdPathIdPathToStopPointId

