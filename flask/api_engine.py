import json
import requests
# import connections
import connections_sqlalchemy


# query finnhub to get ticker data
def get_data(symbol):
    
    # so far we only use finnhub api therefore no need to give options for different tokens
    header = {
        'X-Finnhub-Token':'ckp0ajpr01qlsp907g8gckp0ajpr01qlsp907g90'
        }
    
    return requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol}', headers = header)
