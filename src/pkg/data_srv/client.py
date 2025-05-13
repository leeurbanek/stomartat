"""src/pkg/data_srv/client.py\n
get_ohlc_data(ctx) - fetch OHLC data\n
"""
import logging

from pathlib import Path

from pkg.data_srv.process import DataProcessor
from pkg import DEBUG


logger = logging.getLogger(__name__)


def get_ohlc_data(ctx:dict, symbol:str)->None:
    """Direct workflow of client"""
    if DEBUG: logger.debug(f"get_ohlc_data(ctx={ctx}, symbol={symbol})")

    # check 'data' folder exists in users 'work_dir', if not create folder
    Path(f"{ctx['default']['work_dir']}/data").mkdir(parents=True, exist_ok=True)

    # select data provider and get data
    if ctx['data_service']['data_provider'] == "tiingo":
        from pkg.data_srv.reader import TiingoReader
        use_tiingo = TiingoReader(ctx=ctx)
        data = use_tiingo.data_reader(symbol=symbol)
    elif ctx['data_service']['data_provider'] == "yahoo":
        pass

    # create price, volume, etc. dataframe for one symbol
    df = _create_dataframe_for_symbol(ctx=ctx, data=data)
    if DEBUG: logger.debug(f"dataframe for {symbol}:\n{df}\ncolumns: {list(df.columns)}")

    # if not DEBUG: print('\nBegin download')
    # if not DEBUG: print(' finished!')
    # if not DEBUG: print(f" Saved to: '{ctx['default']['work_dir']}data'\n")


def _create_dataframe_for_symbol(ctx:dict, data:tuple)->None:
    """"""
    if DEBUG: logger.debug(f"_create_dataframe_for_symbol(ctx={type(ctx)}, data={type(data)})")
    start = DataProcessor(ctx=ctx, data=data)
    return start.process_dataframe()
