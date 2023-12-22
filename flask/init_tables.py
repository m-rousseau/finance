from sqlalchemy import create_engine, text, URL, MetaData, Table, Column, BigInteger, Date, Double, Integer, String


# create all base tables
def create_tables():

    meta = MetaData()

    # list out all tables to be created

    # stock data
    Table(
        'stocks', meta,
        Column('pk', String, primary_key=True),
        Column('ticker', String),
        Column('open', Double),
        Column('close', Double),
        Column('low', Double),
        Column('high', Double),
        Column('vwap', Double),
        Column('volume', Double),
        Column('eodtimestamp', BigInteger),
        Column('date', Date)
    )
            
    # treasury -- USA
    Table(
        'treasury_debt_to_penny', meta,
        Column('record_date', String, primary_key=True),
        Column('debt_held_public_amt', Double),
        Column('intragov_hold_amt', Double),
        Column('tot_pub_debt_out_amt', Double)
    )    
    
    # return metadata object that contains all tables to be created
    return meta