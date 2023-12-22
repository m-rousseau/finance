from sqlalchemy import text
from datetime import datetime, timedelta
import pandas as pd


# get stock data
def get_previous_stock_data(external_api, tickers=[]):

    results = []
    for ticker in tickers:
        result = external_api.get_previous_close_agg(ticker=ticker)
        # since there is only 1 element in the array, unnest
        results.append(result[0])
    
    return results


# used to backfill all historical data
def get_historical_stock_data(external_api, tickers=[], backfill=False):

    # determine how far back to query
    if backfill:
        from_date_delta = 1095
    else:
        from_date_delta = 1

    df_all = pd.DataFrame()
    for ticker in tickers:
        # create temp dataframe for all historical data (1 year to today)
        df_ticker = pd.DataFrame(external_api.list_aggs(
            ticker=ticker, 
            multiplier=1, 
            timespan="day", 
            from_=datetime.today() - timedelta(days=from_date_delta), 
            to=datetime.today().strftime("%Y-%m-%d"), 
            limit=50000
            ))
        # add column with ticker
        df_ticker['ticker'] = ticker
        # append dataframe to complete dataframe
        df_all = pd.concat([df_all, df_ticker])

    return df_all


# rename and re-organize columns of dataframe in preperation for insertion
def clean_up_stock_data(df_upload):

    # add date as column
    df_upload['date'] = df_upload['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d'))

    # add primary key column and renamed timestamp column
    df_upload['pk'] = df_upload['date'] + df_upload['ticker']
    df_upload['eodtimestamp'] = df_upload['timestamp']

    # re-arragne columns
    return df_upload[['pk', 'ticker', 'open', 'close', 'low', 'high', 'vwap', 'volume', 'eodtimestamp', 'date']]


# clean stock data rows prior to insert
def delete_table_data(db_connection, df_upload, table_name, primarykey):

    # get the primary keys of the data being uploaded
    df_primary_keys = df_upload[[primarykey]]

    # delete all rows of data with corresponding primary key
    # can only have a single primary key
    for values in df_primary_keys.values:
        for value in values:
            deleteStatement = text(f"DELETE FROM {table_name} where {primarykey} = '{value}'")
            db_connection.execute(deleteStatement)
    db_connection.commit()
    db_connection.close()


# write the stock data to database
def write_data(db_engine, df, table_name):
    df.to_sql(table_name, con=db_engine, if_exists='append', index=False)
