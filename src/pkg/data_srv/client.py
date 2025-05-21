"""src/pkg/data_srv/client.py\n
fetch_indicator_data(ctx) - fetch OHLC data\n
"""
import logging

from pkg import DEBUG
from pkg.data_srv import process, utils


logger = logging.getLogger(__name__)


def fetch_indicator_data(ctx:dict, symbol:str)->None:
    """Save data used for calculating indicators. Directs workflow of client"""
    if DEBUG: logger.debug(f"fetch_indicator_data(ctx={ctx}, symbol={symbol})")

    # select data provider and get data
    data = _select_data_provider(ctx=ctx, symbol=symbol)

    # create price, volume, etc. dataframe for one symbol
    df = _create_dataframe_for_symbol(ctx=ctx, data=data)
    if DEBUG: logger.debug(f"dataframe for {symbol}:\n{df}\ncolumns: {list(df.columns)}")

    tuple_list = process.df_to_list_of_tuples(symbol=symbol, df=df)

    db_writer = utils.SqliteWriter(ctx=ctx)
    db_writer.save_indicator_data(tuple_list=tuple_list)

    # add symbol dataframe columns to database
    # utils.add_df_column_data_to_db(ctx=ctx, df=df, symbol=symbol)


    # if not DEBUG: print('\nBegin download')
    # if not DEBUG: print(' finished!')
    # if not DEBUG: print(f" Saved to: '{ctx['default']['work_dir']}data'\n")


def fetch_target_data(ctx:dict)->None:
    """Save ohlc price data for target symbol. Directs workflow of client"""

    symbol, df = _select_data_provider(ctx=ctx, symbol=ctx['interface']['target_data'])
    if DEBUG: logger.debug(f"fetch_target_data(ctx)-> symbol: {symbol}, df:\n{df}")

    tuple_list = process.df_to_list_of_tuples(symbol=symbol, df=df)

    db_writer = utils.SqliteWriter(ctx=ctx)
    db_writer.save_target_data(tuple_list=tuple_list)


def _create_dataframe_for_symbol(ctx:dict, data:tuple)->None:
    """"""
    if DEBUG: logger.debug(f"_create_dataframe_for_symbol(ctx={type(ctx)}, data={type(data)})")
    start = process.DataProcessor(ctx=ctx, data=data)
    return start.process_dataframe()


def _select_data_provider(ctx:dict, symbol:str)->object:
    if ctx['data_service']['data_provider'] == "tiingo":
        from pkg.data_srv.reader import TiingoReader
        use_tiingo = TiingoReader(ctx=ctx)
        data = use_tiingo.data_reader(symbol=symbol)
    elif ctx['data_service']['data_provider'] == "yahoo":
        pass
    return data
