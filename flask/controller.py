import api_engine as a
import connections_sqlalchemy as cs
from sqlalchemy import text
import pandas as pd


# get json data from finnhub
r = a.get_data('AAPL')
df = pd.DataFrame(r.json(), index=[0])

engine = cs.get_connection()

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("select ticker from stocks")
            )
        for row in result:
            print("ticker:", row.ticker)
except Exception as ex:
        print("Sorry your connection is not created some interruption is occured please check and try it again \n", ex)            