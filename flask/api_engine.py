from configparser import ConfigParser
from polygon import RESTClient
from datetime import datetime
import os

# we use polygon.io -- https://polygon.io/

def create_client(filename='creds.ini', section='apikeys'):
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


# api_client = config()

# ticker = "AAPL"

# # OCHL data

# aggs = []
# tickers = ['AAPL', 'TSLA']
# for ticker in tickers:
#     for a in api_client.get_previous_close_agg(ticker=ticker):
#         aggs.append(a)

# print(aggs)

