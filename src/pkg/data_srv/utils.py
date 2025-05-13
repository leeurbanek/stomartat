"""src/pkg/data_srv/utils.py\n
"""
import logging

from pkg import DEBUG
from pkg.ctx_mgr import SqliteConnectManager


logger = logging.getLogger(__name__)


def sqlite_create_database(ctx:dict, mode:str):
    """"""
    if DEBUG: logger.debug(f"create_database(ctx={type(ctx)}, mode={mode})")

    col_list = ctx['interface']['arguments']
    table_list = ctx['interface']['data_line']

    with SqliteConnectManager(ctx=ctx, mode=mode) as db:
        # create table for each data line
        for table in table_list:
            db.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table} (
                    Date    INTEGER    NOT NULL,
                    PRIMARY KEY (Date)
                )
                WITHOUT ROWID
            ''')
            # add symbol column to table
            try:
                for col in col_list:
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
