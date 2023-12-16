import api_engine as a
import connections_sqlalchemy as cs
from sqlalchemy import text
from datetime import datetime
import pandas as pd


# get stock data
def get_stock_data(api_engine, tickers=[]):
    results = []
    for ticker in tickers:
        r = api_engine.get_previous_close_agg(ticker=ticker)
        # since there is only 1 element in the array, unnest
        results.append(r[0])
    
    return results


# outward facing api engine
api_engine = a.create_client()
# inward facing db engine
db_engine = cs.get_connection()
db_connection = db_engine.connect()

# get basic data for apple
test = get_stock_data(api_engine, ['AAPL', 'TSLA', 'GME'])
df = pd.DataFrame(test)
# add date as column
df['date'] = df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d'))
# add primary key column and renamed timestamp column
df['pk'] = df['date'] + df['ticker']
df['eodtimestamp'] = df['timestamp']
# re-arragne columns
df2 = df[['pk', 'ticker', 'open', 'close', 'low', 'high', 'vwap', 'volume', 'eodtimestamp', 'date']]
# clean data rows prior to insert
df_primary_keys = df[['pk']]
for key in df_primary_keys.pk.to_list():
    deleteStatement = text(f"DELETE FROM stocks where pk = '{key}'")
    db_connection.execute(deleteStatement)
db_connection.commit()
db_connection.close()

# append data to database
df2.to_sql('stocks', con=db_engine, if_exists='replace', index=False)
print(df2)
# database thread
# try:
#     with engine.connect() as connection:
#         result = connection.execute(
#             text("select ticker from stocks")
#             )
#         for row in result:
#             print("ticker:", row.ticker)
# except Exception as ex:
#         print("Sorry your connection is not created some interruption is occured please check and try it again \n", ex)            