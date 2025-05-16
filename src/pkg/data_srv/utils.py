"""src/pkg/data_srv/utils.py\n
"""
import logging

import pandas as pd

from pkg import DEBUG
from pkg.ctx_mgr import SqliteConnectManager


logger = logging.getLogger(__name__)


class SqliteWriter:
    """"""
    def __init__(self, ctx):
        self.ctx = ctx

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"ctx=({type(self.ctx)})"
        )

    def save_data(self, symbol, tuple_list):
        """"""
        if DEBUG: logger.debug(f"{self}.save_data(\nsymbol={symbol}, tuple_list={tuple_list}\n)")

        for row in tuple_list:
            if DEBUG: logger.debug(f"name: {type(row).__name__}, tuple: {row},")

        # with SqliteConnectManager(db_path=self.db_path, mode='rwc') as db:
        #     for row in close_location_value(gen):
        #         table = {type(row).__name__.lower()}.pop()
        #         symbol = {row.symbol}.pop()
        #         date = {row.date}.pop()
        #         clv = {row.clv}.pop()
        #         if not bool(idx):
        #             db.cursor.execute(f'''
        #                 INSERT INTO {table} (Date, {symbol})
        #                 VALUES (?, ?)''', (date, clv)
        #             )
        #         else:
        #             db.cursor.execute(f'''
        #                 UPDATE {table} SET {symbol} = ?
        #                 WHERE Date = {date}''', (clv,)
        #             )


def add_df_column_data_to_db(ctx:dict, df:pd.DataFrame, symbol:str)->None:
    """"""
    if DEBUG: logger.debug(f"add_df_column_data_to_db(\nctx={type(ctx)},\ndf={df},\nsymbol={symbol})")

    with SqliteConnectManager(ctx=ctx, mode='rw') as db:
        for col in df.columns:
            s = df[col]
            print(f"name: {s.name}, values: {s.values},\nindex: {s.index}")


def sqlite_create_database(ctx:dict)->None:
    """"""
    if DEBUG: logger.debug(f"create_database(ctx={type(ctx)})")

    with SqliteConnectManager(ctx=ctx, mode='rwc') as db:
        # create table for each data line
        for table in ctx['interface']['data_line']:
            db.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table} (
                    Date    INTEGER    NOT NULL,
                    PRIMARY KEY (Date)
                )
                WITHOUT ROWID
            ''')
            # add symbol column to table
            try:
                for col in ctx['interface']['arguments']:
                    db.cursor.execute(f'''
                        ALTER TABLE {table} ADD COLUMN {col} INTEGER
                    ''')
            except db.sqlite3.Error as e:
                logger.debug(f"ERROR, table '{table}' {e}")

    if not DEBUG: print(f" created db: '{db.db_path}'")


def verify_data_folder_exists(ctx:dict)->None:
    """"""
    from pathlib import Path

    if DEBUG: logger.debug(f"verify_data_folder_exists(ctx={type(ctx)})")

    Path(f"{ctx['default']['work_dir']}/data").mkdir(parents=True, exist_ok=True)
