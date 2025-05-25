"""src/pkg/data_srv/utils.py\n
class SqliteWriter\n
sqlite_create_database(ctx)\n
verify_data_folder_exists(ctx)
"""
import logging

from pathlib import Path

from pkg import DEBUG
from pkg.ctx_mgr import SqliteConnectManager


logger = logging.getLogger(__name__)


class SqliteWriter:
    """"""
    def __init__(self, ctx):
        self.ctx = ctx
        self.index = ctx['interface']['index']
        self.table_list = ctx['interface']['data_line']


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"ctx=({type(self.ctx)})"
        )

    def save_indicator_data(self, tuple_list:list[tuple])->None:
        """"""
        if DEBUG: logger.debug(f"db_writer.save_indicator_data(tuple_list={tuple_list})")

        with SqliteConnectManager(ctx=self.ctx, mode='rwc') as db:
            for row in tuple_list:
                symbol = type(row).__name__  # ticker symbol for current data
                date = row.Index  # index for current row (tuples 'Date' field)
                # table_list = row._fields[1:]  # data from row excluding 'Date' field
                try:
                    # for table in table_list:
                    for table in self.table_list:
                        table = table.lower()
                        value = getattr(row, table)
                        if self.index == 0:
                            query = f"INSERT INTO {table} (Date, {symbol}) VALUES (?, ?)"
                            db.cursor.execute(query, (date, value))
                        else:
                            db.cursor.execute(f"UPDATE {table} SET {symbol} = ? WHERE Date = {date}", (value,))
                except db.sqlite3.Error as e:
                    if DEBUG: logger.debug(f" {e}")


    def save_target_data(self, tuple_list:list[tuple])->None:
        """"""
        if DEBUG: logger.debug(f"db_writer.save_target_data(tuple_list={tuple_list})")

        with SqliteConnectManager(ctx=self.ctx, mode='rwc') as db:
            try:
                for row in tuple_list:
                    table = type(row).__name__
                    date = row[0]
                    data = row[1:]
                    query = f"INSERT INTO {table} (Date, Open, High, Low, Close, Volume) VALUES (?, ?, ?, ?, ?, ?)"
                    # if DEBUG: logger.debug(f"query: {query}")
                    db.cursor.execute(query, (date, *data))
            except db.sqlite3.Error as e:
                if DEBUG: logger.debug(f" {e}")


def sqlite_create_database(ctx:dict)->None:
    """Create sqlite3 database. Tables are data lines, columns are ticker symbols."""
    if DEBUG: logger.debug(f"create_database(ctx={type(ctx)})")

    # if old database exists remove it
    Path(f"{ctx['default']['work_dir']}/data/{ctx['interface']['database']}").unlink(missing_ok=True)

    with SqliteConnectManager(ctx=ctx, mode='rwc') as db:
        try:
            # create table for each indicator (data line)
            for table in ctx['interface']['data_line']:
                db.cursor.execute(f'''
                    CREATE TABLE {table.lower()} (
                        Date    INTEGER    NOT NULL,
                        PRIMARY KEY (Date)
                    )
                    WITHOUT ROWID
                ''')
                # add column for each symbol to data line table
                for col in ctx['interface']['arguments']:
                    db.cursor.execute(f'''
                        ALTER TABLE {table} ADD COLUMN {col} INTEGER
                    ''')
            # create table for target symbol (ohlc prices)
            for table in ctx['interface']['target_data']:
                db.cursor.execute(f'''
                    CREATE TABLE {table} (
                        Date      INTEGER    NOT NULL,
                        Open      INTEGER    NOT NULL,
                        High      INTEGER    NOT NULL,
                        Low       INTEGER    NOT NULL,
                        Close     INTEGER    NOT NULL,
                        Volume    INTEGER    NOT NULL,
                        PRIMARY KEY (Date)
                    )
                    WITHOUT ROWID
                ''')
        except Exception as e:
            if DEBUG: logger.debug(f" {e}")

    if not DEBUG: print(f" created db: '{db.db_path}'")


def verify_data_folder_exists(ctx:dict)->None:
    """Create `data` folder in work directory if it does not exist."""

    if DEBUG: logger.debug(f"verify_data_folder_exists(ctx={type(ctx)})")
    Path(f"{ctx['default']['work_dir']}/data").mkdir(parents=True, exist_ok=True)
