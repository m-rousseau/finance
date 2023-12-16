from configparser import ConfigParser
from polygon import RESTClient
import os

# we use polygon.io -- https://polygon.io/

def config(filename='creds.ini', section='apikeys'):
    # get relative path
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, filename)
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section
    api_client = None
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            if param[0] == 'apikey':
                api_client = RESTClient(api_key=param[1])
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return api_client


api_client = config()

ticker = "AAPL"

# List Aggregates (Bars)
aggs = []
for a in api_client.list_aggs(ticker=ticker, multiplier=1, timespan="minute", from_="2023-01-01", to="2023-06-13", limit=50000):
    aggs.append(a)

print(aggs)