import sqlite3
import datetime
from pathlib import Path
import os

from apperone.app_config import AppConfig
from apperone.output import log


class AppTime:
    def __init__(self, database):
        self.database = Path(database).expanduser()
        os.makedirs(self.database.parent.as_posix(), exist_ok=True)
        log(f"Database: {self.database}")

    def increase_times(self, app: AppConfig):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.database)

        self.create_tables(conn)

        cursor = conn.cursor()

        current_date = datetime.date.today().strftime('%Y-%m-%d')

        # Get the app_uid for the given app or insert a new entry if it doesn't exist
        cursor.execute('SELECT app_uid FROM app_id WHERE app_id = ?', (app.app_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('INSERT INTO app_id (app_id) VALUES (?)', (app.app_id,))
            app_uid = cursor.lastrowid
        else:
            app_uid = result[0]

        # Increase the time in app_time table
        cursor.execute('SELECT time FROM app_time WHERE app_uid = ? and date = ?', (app_uid, current_date))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('INSERT INTO app_time (app_uid, time, date) VALUES (?, ?, ?)', (app_uid, 1, current_date))
        cursor.execute('UPDATE app_time SET time = time + 1 WHERE app_uid = ? and date = ?', (app_uid, current_date))

        # Insert new groups if they don't exist and get their group_uids
        group_uids = []
        for group in app.groups:
            cursor.execute('SELECT group_uid FROM `group` WHERE `group` = ?', (group,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute('INSERT INTO `group` (`group`) VALUES (?)', (group,))
                group_uids.append(cursor.lastrowid)
            else:
                group_uids.append(result[0])

        # Increase the time in group_time and app_time for each matching app_id and group
        for group_uid in group_uids:
            # Increase the time in group_time table
            cursor.execute('SELECT time FROM group_time WHERE group_uid = ? and date = ?', (group_uid, current_date))
            result = cursor.fetchone()
            if result is None:
                cursor.execute('INSERT INTO group_time (group_uid, time, date) VALUES (?, ?, ?)',
                               (group_uid, 1, current_date))
            cursor.execute('UPDATE group_time SET time = time + 1 WHERE group_uid = ? and date = ?',
                           (group_uid, current_date))

        ret_val = self.has_time(app, conn)

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        return ret_val

    def create_tables(self, conn=None):
        if conn is None:
            conn = sqlite3.connect(self.database)
            close_conn = True
        else:
            close_conn = False

        cursor = conn.cursor()

        # Create the necessary tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_id (
                app_uid INTEGER PRIMARY KEY,
                app_id TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `group` (
                group_uid INTEGER PRIMARY KEY,
                `group` TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_time (
                app_uid INTEGER PRIMARY KEY,
                time INTEGER DEFAULT 0,
                date TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_time (
                group_uid INTEGER PRIMARY KEY,
                time INTEGER DEFAULT 0,
                date TEXT
            )
        ''')

        conn.commit()
        if close_conn:
            conn.close()

    def has_time(self, app: AppConfig, conn=None):
        if conn is None:
            conn = sqlite3.connect(self.database)
            close_conn = True
        else:
            close_conn = False

        cursor = conn.cursor()

        # Get the app_uid for the given app or insert a new entry if it doesn't exist
        cursor.execute('SELECT app_uid FROM app_id WHERE app_id = ?', (app.app_id,))
        result = cursor.fetchone()
        if result is None:
            log(f"Unknown app {app.app_id}")
            return True
        else:
            app_uid = result[0]

        # Increase the time in app_time table
        cursor.execute('SELECT time FROM app_time WHERE app_uid = ?', (app_uid,))
        result = cursor.fetchone()
        if result is None:
            log(f"Unknown app time {app.app_id}")
            return True

        conn.commit()
        if close_conn:
            conn.close()

        log(f"{app.app_id} has {app.time - result[0]}min left")
        return app.time > result[0]
