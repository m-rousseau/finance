from configparser import ConfigParser
from polygon import RESTClient
import finnhub
import os

# APIs used:
    # FINNHUB: https://finnhub.io/docs/api/library
    # POLYGON: https://polygon.io/
    # GOV: https://fiscaldata.treasury.gov/api-documentation/
    # FED: 

def create_client(filename='creds.ini', api_name=''):
    
    # get relative path
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, filename)
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section
    api_client = None
    if parser.has_section('apikey'):
        params = parser.items('apikey')
        for param in params:
            if param[0] == api_name:
                if api_name == 'polygon':
                    api_client = RESTClient(api_key=param[1])
                if api_name == 'finnhub':
                    api_client = finnhub.Client(api_key=param[1])
        
        return api_client
    
    else:
        raise Exception('Section {0} not found in the {1} file'.format(api_name, filename))

    
