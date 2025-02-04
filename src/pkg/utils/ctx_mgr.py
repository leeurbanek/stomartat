import logging
import sqlite3
import os
import sys
import threading
import time
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src import config_file


conf_obj = ConfigParser()
conf_obj.read(config_file)

logging.getLogger('selenium').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

ADBLOCK = conf_obj['Scraper']['adblock']
DRIVER = conf_obj['Scraper']['driver']


class DatabaseConnectionManager:
    """Context manager for Sqlite3 databases.
    -----------------------------------------
    Commits changes on exit.\n
    Parameters
    ----------
    `db_path` : string
        Path to an Sqlite3 database (default='test.db' for in memory db).\n
    `mode` : string
        determines if the new database is opened read-only 'ro', read-write 'rw',\n
        read-write-create 'rwc', or pure in-memory database 'memory' (default) mode.\n
    Returns
    -------
    An Sqlite3 connection object.\n
    """
    def __init__(self, db_path='test.db', mode='memory'):
        self.db_path = db_path
        self.mode = mode

    def __enter__(self):
        logger.debug('DatabaseConnectionManager.__enter__()')
        try:
            self.connection = sqlite3.connect(
                f'file:{os.path.abspath(self.db_path)}?mode={self.mode}',
                # detect_types=sqlite3.PARSE_DECLTYPES, uri=True
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, uri=True
            )
            self.cursor = self.connection.cursor()
            logger.debug(f"connected '{os.path.basename(self.db_path)}', mode: {self.mode}")
            # return self.cursor
            return self
        except sqlite3.Error as e:
            print(f'{e}: {self.db_path}')

    def __exit__(self, exc_type, exc_value, exc_traceback):
        logger.debug('DatabaseConnectionManager.__exit__()')
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


class SpinnerManager:
    """Manage a simple spinner object"""
    busy = False
    delay = 0.2

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, debug: bool=None, delay=None):
        self.debug = debug
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        # print(f"debug: {self.debug}")
        if self.debug: logger.debug(f"SpinnerManager(debug={self.debug}).__enter__()")
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if self.debug: logger.debug(f"SpinnerManager(debug={self.debug}).__exit__()")
        if exception is not None:
            return False


class WebDriverManager:
    """Manage Selenium web driver"""
    def __init__(self, debug: bool) -> None:
        self.debug = debug

    def __enter__(self):
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.headless = True  # don't display browser window
        s = Service(DRIVER)
        self.driver = webdriver.Chrome(service=s, options=chrome_opts)
        # Install ad blocker if used
        if os.path.exists(ADBLOCK):
            self.driver.install_addon(ADBLOCK)
            # pyautogui.PAUSE = 2.5
            # pyautogui.click()  # position browser window
            # pyautogui.hotkey('ctrl', 'w')  # close ADBLOCK page

        if self.debug: logger.debug(f'WebDriverManager.__enter__(session={self.driver.session_id})')
        return self.driver

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.quit()
        if self.debug: logger.debug('WebDriverManager.__exit__()')


if __name__ == '__main__':
    import unittest

    class SpinnerManagerTest(unittest.TestCase):
        def test_spinner_manager(self):
            with SpinnerManager(debug=True) as spinner:
                time.sleep(2)  # some long-running operation


    class ContextManagerTest(unittest.TestCase):
        def setUp(self) -> None:
            self.db_table = 'data'
            self.rows = [
                ('D1','F1'), ('D2','F2'), ('D3','F3'),
            ]

        def test_db_ctx_mgr_in_memory_mode(self):
            with DatabaseConnectionManager() as db:
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

    unittest.main()
