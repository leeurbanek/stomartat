# python -m unittest test/test_ctx_mgr.py -v
import time
import unittest

from pkg.ctx_mgr import SpinnerManager, SqliteConnectManager
from test.data import ctx


class SpinnerManagerTest(unittest.TestCase):
    def test_spinner_manager(self):
        with SpinnerManager() as spinner:
            time.sleep(2)  # some long-running operation


class ContextManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db_table = 'data'
        self.rows = [
            ('D1','F1'), ('D2','F2'), ('D3','F3'),
        ]

    def test_db_ctx_mgr_in_memory_mode(self):
        with SqliteConnectManager(ctx=ctx, mode='memory') as db:
            db.cursor.execute(f'''
                CREATE TABLE {self.db_table} (
                    Date    DATE        NOT NULL,
                    Field   INTEGER     NOT NULL,
                    PRIMARY KEY (Date)
                );
            ''')
            db.cursor.executemany(f'INSERT INTO {self.db_table} VALUES (?,?)', self.rows)
            try:
                sql = db.cursor.execute(f"SELECT Field FROM {self.db_table} WHERE ROWID IN (SELECT max(ROWID) FROM {self.db_table});")
                result = sql.fetchone()
            except Exception as e:
                print(f"{e}")
            self.assertEqual(result, ('F3',))


if __name__ == '__main__':
    unittest.main()
