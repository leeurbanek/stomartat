"""src/pkg/data_srv/utils.py\n
class SqliteWriter\n
sqlite_create_database(ctx)\n
verify_data_folder_exists(ctx)
"""
import logging

# import pandas as pd

from pkg import DEBUG
from pkg.ctx_mgr import SqliteConnectManager


logger = logging.getLogger(__name__)


class SqliteWriter:
    """"""
    def __init__(self, ctx):
        self.ctx = ctx
        self.data_line = ctx['interface']['data_line']

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"ctx=({type(self.ctx)})"
        )

    # def save_data(self, symbol:str, tuple_list:list[tuple])->None:
    def save_data(self, tuple_list:list[tuple])->None:
        """"""
        if DEBUG: logger.debug(f"db_writer.save_data(tuple_list={type(tuple_list)})")

        for row in tuple_list:
            symbol = type(row).__name__
            index = row.Index
            data_line = row._fields[1:]
            # for dl in self.data_line:
            for dl in data_line:
                if DEBUG: logger.debug(f"{symbol}, {index}, {dl}, {getattr(row, dl)}")

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



# You can use SQL functionality insert or replace

# query=''' insert or replace into NewTable (ID,Name,Age) values (?,?,?) '''
# conn.executemany(query, test.to_records(index=False))
# conn.commit()

# Thanks, this works. Minor addition: the index is excluded from the record array to match the table structure. conn.executemany(query,test.to_records(index=False)) –

# That's right. I usually use primary key as index in df, so I forgot that. –

# Getting a binary data column instead of datetime when I use this. –

# Is there any way to push the entire pandas dataframe as a whole rather than needing to write out the individual values? It looks like with the query code that you need to explicitly write the individual values: insert or replace into NewTable (ID,Name,Age) values (?,?,?) –


# def add_df_column_data_to_db(ctx:dict, df:pd.DataFrame, symbol:str)->None:
#     """"""
#     if DEBUG: logger.debug(f"add_df_column_data_to_db(\nctx={type(ctx)},\ndf={df},\nsymbol={symbol})")

#     with SqliteConnectManager(ctx=ctx, mode='rw') as db:
#         for col in df.columns:
#             s = df[col]
#             print(f"name: {s.name}, values: {s.values},\nindex: {s.index}")


def sqlite_create_database(ctx:dict)->None:
    """Create sqlite3 database. Tables are data lines, columns are ticker symbols."""
    if DEBUG: logger.debug(f"create_database(ctx={type(ctx)})")

    with SqliteConnectManager(ctx=ctx, mode='rwc') as db:
        # create table for each data line
        for table in ctx['interface']['data_line']:
            db.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table.lower()} (
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
                logger.debug(f"ERROR, table '{table.lower()}' {e}")

    if not DEBUG: print(f" created db: '{db.db_path}'")


def verify_data_folder_exists(ctx:dict)->None:
    """Create `data` folder in work directory if it does not exist."""
    from pathlib import Path

    if DEBUG: logger.debug(f"verify_data_folder_exists(ctx={type(ctx)})")

    Path(f"{ctx['default']['work_dir']}/data").mkdir(parents=True, exist_ok=True)
