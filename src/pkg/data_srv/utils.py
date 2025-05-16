"""src/pkg/data_srv/utils.py\n
class SqliteWriter\n
sqlite_create_database(ctx)\n
verify_data_folder_exists(ctx)
"""
import logging

from pkg import DEBUG
from pkg.ctx_mgr import SqliteConnectManager


logger = logging.getLogger(__name__)


class SqliteWriter:
    """"""
    def __init__(self, ctx):
        self.ctx = ctx
        self.data_table_list = ctx['interface']['data_line']

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"ctx=({type(self.ctx)})"
        )

    def save_data(self, tuple_list:list[tuple])->None:
        """"""
        if DEBUG: logger.debug(f"db_writer.save_data(tuple_list={tuple_list})")

        with SqliteConnectManager(ctx=self.ctx, mode='rw') as db:
            for row in tuple_list:
                symbol = type(row).__name__  # ticker symbol for current data
                index = row.Index  # index for current row (tuple 'Date' field)
                data_table_list = row._fields[1:]  # data from row excluding 'Date' field (index)
                try:
                    # for table in self.data_table_list:
                    for table in data_table_list:
                        value = getattr(row, table)
                        # if DEBUG: logger.debug(f"{symbol} {type(symbol)} {table} {type(table)} Date: {index} {type(index)} value: {value} {type(value)}")
                        if DEBUG: logger.debug(f"\nINSERT OR REPLACE INTO {table} (Date, {symbol}) VALUES ({index}, {value})")
                        query = f"INSERT OR REPLACE INTO {table} (Date, {symbol}) VALUES (?, ?)"
                        db.cursor.execute(query, (index, value))
                except db.sqlite3.Error as e:
                    if DEBUG: logger.debug(f"ERROR, {symbol} {table.lower()} {e}")

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
                # logger.debug(f"ERROR, table '{table.lower()}' {e}")
                pass

    if not DEBUG: print(f" created db: '{db.db_path}'")


def verify_data_folder_exists(ctx:dict)->None:
    """Create `data` folder in work directory if it does not exist."""
    from pathlib import Path

    if DEBUG: logger.debug(f"verify_data_folder_exists(ctx={type(ctx)})")

    Path(f"{ctx['default']['work_dir']}/data").mkdir(parents=True, exist_ok=True)
