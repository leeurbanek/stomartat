"""src/pkg/data_srv/client.py\n
fetch_indicator_data(ctx) - fetch OHLC data\n
"""
import logging

from pkg import DEBUG
from pkg.data_srv import process, utils


logger = logging.getLogger(__name__)


def fetch_indicator_data(ctx:dict)->None:
    """Data for calculating indicators i.e. clv, price, volume etc."""
    if DEBUG: logger.debug(f"fetch_indicator_data(ctx={type(ctx)})")

    # create database
    utils.create_sqlite_indicator_database(ctx=ctx)

    # select data provider
    processor = _select_data_provider(ctx=ctx)

    # get and save data for each ticker
    for index, ticker in enumerate(ctx['interface']['arguments']):
        ctx['interface']['index'] = index
        data_tuple = processor.download_and_parse_price_data(ticker=ticker)
        utils.write_indicator_data_to_sqlite_db(ctx=ctx, data_tuple=data_tuple)


def fetch_target_data(ctx:dict, symbol:str)->None:
    """ohlc price data for target symbol."""
    if DEBUG: logger.debug(f"fetch_target_data(ctx: {type(ctx)}, symbol: {symbol})")

    _, df = _select_data_provider(ctx=ctx, symbol=symbol)

    tuple_list = process.df_to_list_of_tuples(symbol=symbol, df=df)

    db_writer = utils.SqliteWriter(ctx=ctx)
    db_writer.save_target_data(tuple_list=tuple_list)


def _create_dataframe_for_symbol(ctx:dict, data:tuple)->None:
    """"""
    if DEBUG: logger.debug(f"_create_dataframe_for_symbol(ctx={type(ctx)}, data={data})")
    start = process.DataProcessor(ctx=ctx, data=data)
    return start.process_dataframe()


def _select_data_provider(ctx:dict)->object:
    """"""
    if DEBUG: logger.debug(f"_select_data_provider(ctx={ctx})")

    # if ctx['data_service']['data_provider'] == "alphavantage":
    #     from pkg.data_srv.reader import AlphaVantageReader
    #     reader = AlphaVantageReader(ctx=ctx)
    #     data = reader.get_ticker_df_tuple(ticker=symbol)

    # elif ctx['data_service']['data_provider'] == "tiingo":
    #     from pkg.data_srv.reader import TiingoReader
    #     reader = TiingoReader(ctx=ctx)
    #     data = reader.get_ticker_df_tuple(ticker=symbol)

    # elif ctx['data_service']['data_provider'] == "yfinance":
    #     from pkg.data_srv.reader import YahooFinanceReader
    #     reader = YahooFinanceReader(ctx=ctx)
    #     data = reader.get_ticker_df_tuple(ticker=symbol)

    # return data

    match ctx['data_service']['data_provider']:
        case "alphavantage":
            from pkg.data_srv.agent import AlphaVantageDataProcessor
            return AlphaVantageDataProcessor(ctx=ctx)
        case "tiingo":
            from pkg.data_srv.agent import TiingoDataProcessor
            return TiingoDataProcessor(ctx=ctx)
        case "yfinance":
            from pkg.data_srv.agent import YahooFinanceDataProcessor
            return YahooFinanceDataProcessor(ctx=ctx)
        case _:  # Pattern not attempted
            pass
