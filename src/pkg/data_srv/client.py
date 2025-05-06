"""src/pkg/data_srv/client.py\n
get_ohlc_data(ctx) - fetch OHLC data\n
"""
import logging

from pathlib import Path

from pkg import DEBUG


logger = logging.getLogger(__name__)

def get_ohlc_data(ctx):
    """Check if `data` folder exists. Direct workflow of client"""
    if DEBUG: logger.debug(f"get_ohlc_data(ctx={type(ctx)})")

    # check 'data' folder exists in users 'work_dir', if not create folder
    Path(f"{ctx['default']['work_dir']}/data").mkdir(parents=True, exist_ok=True)

    if not DEBUG: print('\nBegin download')
    df = _download_data(ctx=ctx)
    _process_data(df=df)
    if not DEBUG: print(' finished!')
    if not DEBUG: print(f" Saved to: '{ctx['default']['work_dir']}data'\n")


def _download_data(ctx):
    """"""
    if DEBUG: logger.debug(f"_download_data(ctx={ctx})")

    # select data provider
    if ctx['data_service']['data_provider'] == "tiingo":
        from pkg.data_srv.reader import TiingoReader
        tiingo = TiingoReader(ctx)
        df = tiingo.data_reader()
    else:
        pass
    return df


def _process_data(df):
    """"""
    if DEBUG: logger.debug(f"_process_data(df={df})")
