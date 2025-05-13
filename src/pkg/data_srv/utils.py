"""src/pkg/data_srv/utils.py\n
"""
import logging

from pkg import DEBUG
from pkg.ctx_mgr import SqliteConnectManager


logger = logging.getLogger(__name__)


def sqlite_create_database(ctx:dict, mode:str):
    """"""
    if DEBUG: logger.debug(f"create_database(ctx={ctx}, mode={mode})")

    import re
    with SqliteConnectManager(ctx=ctx, mode=mode) as db:
        table_list = [t.lower() for t in re.findall(r'[^,;\s]+', ctx['interface']['db_table'])]
        for table in table_list:
            db.cursor.execute(f'''
                CREATE TABLE {table} (
                    Date    INTEGER    NOT NULL,
                    PRIMARY KEY (Date)
                )
            ''')
            # add symbol column to table
            col_list = ctx['interface']['arguments']
            for col in col_list:
                db.cursor.execute(f'''
                    ALTER TABLE {table} ADD COLUMN {col} INTEGER
                ''')
    if not DEBUG: print(f" created db: '{db.db_path}'")
