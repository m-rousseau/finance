import connections_api
import connections_sqlalchemy
import data_management
import pandas as pd
import requests


# dictate which client to use
api_names = {
    'bonds':'finnhub',
    'forex':'polygon',
    'options':'polygon',
    'stocks':'polygon',
    'swaps':'',
}

tickers_bonds = ['']
tickers_stocks = ['GME']
# tickers_stocks = ['AAPL', 'TSLA', 'GME', 'F']


# get bond data
def populate_bond_data(backfill=False):

    # inward facing db engine
    db_engine = connections_sqlalchemy.get_connection()
    db_connection = db_engine.connect()

    gov_url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service'
    if backfill:
        rows = 1095
    else:
        rows = 1

# To Do: nested json dictionaries. Add metadata maybe, or just trim to list?
    gov_metrics = {
        'debt_to_penny': {
            'url': '/v2/accounting/od/debt_to_penny',
            'fields': 'record_date,debt_held_public_amt,intragov_hold_amt,tot_pub_debt_out_amt',
            'filter': '',
            'rows': rows,
            'sort': '-record_date',
            'db_table': 'treasury_debt_to_penny',
            'pk': 'record_date'
        },
        # 'federal_tax_deposits': {
        #     'url': '/v1/accounting/dts/federal_tax_deposits',
        #     'fields': '',
        #     'filter': '',
        # },
        # 'public_debt_transactions': {
        #     'url': '/v1/accounting/dts/public_debt_transactions',
        #     'fields': '',
        #     'filter': '',
        # },
        # 'operating_cash_balance': {
        #     'url': '/v1/accounting/dts/operating_cash_balance',
        #     'fields': '',
        #     'filter': '',
        # },
        # 'federal_maturity_rates': {
        #     'url': '/v1/accounting/dts/federal_maturity_rates',
        #     'fields': '',
        #     'filter': '',
        # },
        # 'statement_net_cost': {
        #     'url': '/v2/accounting/od/statement_net_cost',
        #     'fields': '',
        #     'filter': '',
        # },
    }

    for obj in gov_metrics:
        url = gov_metrics[obj]['url']
        fields = gov_metrics[obj]['fields']
        filter = gov_metrics[obj]['filter']
        rows = gov_metrics[obj]['rows']
        sort = gov_metrics[obj]['sort']
        db_table = gov_metrics[obj]['db_table']
        primarykey = gov_metrics[obj]['pk']
        
        # get data from GOV api
        response = requests.get(f"{gov_url}{url}?fields={fields}&filter={filter}&page[size]={rows}&sort={sort}")
        # save to dataframe
        df = pd.DataFrame(response.json()['data'])
        # clean (delete) data with same primary key
        data_management.delete_table_data(db_connection, df, table_name=db_table, primarykey=primarykey)
        # write data to database
        data_management.write_data(db_engine, df, table_name=db_table)


# get all stock data
def populate_stock_data(backfill=False):
    
    # table name
    table_name = 'stocks'
    primarykey = 'pk'

    # outward facing api engine
    external_api = connections_api.create_client(api_name=api_names[table_name])
    # inward facing db engine
    db_engine = connections_sqlalchemy.get_connection()
    db_connection = db_engine.connect()

    # get all historical data
    df_historical = pd.DataFrame(data_management.get_historical_stock_data(external_api, tickers=tickers_stocks, backfill=backfill))
    df_historical = data_management.clean_up_stock_data(df_historical)

    # get current stock data
    # df_current = pd.DataFrame(data_management.get_previous_stock_data(external_api, tickers=tickers))
    # clean up dataframe
    # df = data_management.clean_up_stock_data(df_current)

    # delete stock data with same primary key
    data_management.delete_table_data(db_connection, df_historical, table_name=table_name, primarykey=primarykey)

    # write data to database
    data_management.write_data(db_engine, df_historical, table_name=table_name)


# run this to make sure all tables have been created
connections_sqlalchemy.initialize_tables()
# query gov bond data
populate_bond_data(backfill=True)
# query stock market data
populate_stock_data(backfill=True)
