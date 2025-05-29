"""src/pkg/data_srv/client.py\n
fetch_indicator_data(ctx) - fetch OHLC data\n
"""
import logging

from pkg import DEBUG
from pkg.data_srv import process, utils


logger = logging.getLogger(__name__)


def fetch_indicator_data(ctx:dict, symbol:str)->None:
    """Save data used for calculating indicators. Directs workflow of client"""
    if DEBUG: logger.debug(f"fetch_indicator_data(ctx={type(ctx)}, symbol={symbol})")

    # select data provider and get data
    data = _select_data_provider(ctx=ctx, symbol=symbol)

    # create price, volume, etc. dataframe for one symbol
    df = _create_dataframe_for_symbol(ctx=ctx, data=data)

    tuple_list = process.df_to_list_of_tuples(symbol=symbol, df=df)

    db_writer = utils.SqliteWriter(ctx=ctx)
    db_writer.save_indicator_data(tuple_list=tuple_list)


def fetch_target_data(ctx:dict, symbol:str)->None:
    """Save ohlc price data for target symbol. Directs workflow of client"""
    if DEBUG: logger.debug(f"fetch_target_data(ctx: {type(ctx)}, symbol: {symbol})")

    _, df = _select_data_provider(ctx=ctx, symbol=symbol)

    tuple_list = process.df_to_list_of_tuples(symbol=symbol, df=df)

    db_writer = utils.SqliteWriter(ctx=ctx)
    db_writer.save_target_data(tuple_list=tuple_list)


def _create_dataframe_for_symbol(ctx:dict, data:tuple)->None:
    """"""
    if DEBUG: logger.debug(f"_create_dataframe_for_symbol(ctx={type(ctx)}, data={type(data)})")
    start = process.DataProcessor(ctx=ctx, data=data)
    return start.process_dataframe()


def _select_data_provider(ctx:dict, symbol:str)->object:
    """"""
    if DEBUG: logger.debug(f"_select_data_provider(ctx={ctx} symbol={symbol})")
    # provider_dict = {
    #     'alphavantage': 'AlphaVantageReader',
    #     'tiingo': 'TiingoReader',
    #     'yfinance': 'YahooFinanceReader'
    # }
    # provider = provider_dict[ctx['data_service']['data_provider']]
    # from pkg.data_srv.reader import provider

    if ctx['data_service']['data_provider'] == "alphavantage":
        pass
    elif ctx['data_service']['data_provider'] == "tiingo":
        from pkg.data_srv.reader import TiingoReader
        reader = TiingoReader(ctx=ctx)
        data = reader.get_symbol_df_tuple(symbol=symbol)
    elif ctx['data_service']['data_provider'] == "yfinance":
        from pkg.data_srv.reader import YahooFinanceReader
        reader = YahooFinanceReader(ctx=ctx)

    return data
