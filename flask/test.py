import finnhub

# Setup client
finnhub_client = finnhub.Client(api_key='ckp0ajpr01qlsp907g8gckp0ajpr01qlsp907g90')

print(finnhub_client.aggregate_indicator('AAPL', 'D'))