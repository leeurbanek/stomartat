"""src/pkg/data_srv/client.py\n
get_ohlc_data(ctx) - fetch OHLC data\n
"""
import logging

from pathlib import Path

from pkg import DEBUG


logger = logging.getLogger(__name__)


def get_ohlc_data(ctx:dict, symbol:str)->None:
    """Check if `data` folder exists. Direct workflow of client"""
    if DEBUG: logger.debug(f"get_ohlc_data(ctx={type(ctx)}, symbol={symbol})")

    # check 'data' folder exists in users 'work_dir', if not create folder
    Path(f"{ctx['default']['work_dir']}/data").mkdir(parents=True, exist_ok=True)

    # select data provider
    if ctx['data_service']['data_provider'] == "tiingo":
        from pkg.data_srv.reader import TiingoReader
        use_tiingo = TiingoReader(ctx)
        data = use_tiingo.data_reader(symbol)
    elif ctx['data_service']['data_provider'] == "yahoo":
        pass

    _process_data(data=data)

    # if not DEBUG: print('\nBegin download')
    # if not DEBUG: print(' finished!')
    # if not DEBUG: print(f" Saved to: '{ctx['default']['work_dir']}data'\n")


def _process_data(ctx:dict, data:tuple)->None:
    """"""
    if DEBUG: logger.debug(f"_process_data(ctx={type(ctx)}, data={data})")
