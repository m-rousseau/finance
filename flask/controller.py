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
tickers_stocks = ['AAPL', 'TSLA', 'GME', 'F']


# get bond data
def populate_bond_data():
    # outward facing api engine
    # external_api = connections_api.create_client(api_name=api_names['bonds'])
    # inward facing db engine
    db_engine = connections_sqlalchemy.get_connection()
    db_connection = db_engine.connect()

    gov_url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service'

# To Do: nested json dictionaries. Add metadata maybe, or just trim to list?
    gov_metrics = {
        'operating_cash_balance':'/v1/accounting/dts/operating_cash_balance',
        'public_debt_transactions':'/v1/accounting/dts/public_debt_transactions',
        'adjustment_public_debt_transactions_cash_basis':'/v1/accounting/dts/adjustment_public_debt_transactions_cash_basis',
        'federal_tax_deposits':'/v1/accounting/dts/federal_tax_deposits',
        'debt_to_penny':'/v2/accounting/od/debt_to_penny',
        'federal_maturity_rates':'/v1/accounting/od/federal_maturity_rates',
        'statement_net_cost':'/v2/accounting/od/statement_net_cost',
        '':'',
        '':'',
        '':'',
        '':'',
        '':'',
        '':'',
    }

    for gm in gov_metrics:
        response = requests.get(f"{gov_url}{gm}")
        print(response.json())


# get all stock data
def populate_stock_data():
    # outward facing api engine
    external_api = connections_api.create_client(api_name=api_names['stocks'])
    # inward facing db engine
    db_engine = connections_sqlalchemy.get_connection()
    db_connection = db_engine.connect()

    # get all historical data
    df_historical = pd.DataFrame(data_management.get_historical_stock_data(external_api, tickers=tickers_stocks))
    df_historical = data_management.clean_up_stock_data(df_historical)

    # get current stock data
    # df_current = pd.DataFrame(data_management.get_previous_stock_data(external_api, tickers=tickers))
    # clean up dataframe
    # df = data_management.clean_up_stock_data(df_current)

    # delete stock data with same primary key
    data_management.delete_stock_data(db_connection, df_historical)

    # write data to database
    data_management.write_data(db_engine, df_historical)

populate_bond_data()