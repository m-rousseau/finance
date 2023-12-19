import connections_api
import connections_sqlalchemy
import data_management
import pandas as pd


# outward facing api engine
external_api = connections_api.create_client()
# inward facing db engine
db_engine = connections_sqlalchemy.get_connection()
db_connection = db_engine.connect()

tickers = ['AAPL', 'TSLA', 'GME']

# get all historical data
df_historical = pd.DataFrame(data_management.get_historical_stock_data(external_api, tickers=tickers))
df_historical = data_management.clean_up_stock_data(df_historical)

# get current stock data
# df_current = pd.DataFrame(data_management.get_previous_stock_data(external_api, tickers=tickers))
# clean up dataframe
# df = data_management.clean_up_stock_data(df_current)

# delete stock data with same primary key
data_management.delete_stock_data(db_connection, df_historical)

# write data to database
data_management.write_data(db_engine, df_historical)
