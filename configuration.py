"""
Module with configuration functions
"""

import os
import sqlite3


def init_db(app):
    """Creates Db if needed"""
    if not os.path.exists(app.config['DATABASE']):
        try:
            conn = sqlite3.connect(app.config['DATABASE'])
            sql_path = os.path.join(app.config['APP_ROOT'], 'db_init.sql')
            cmd = open(sql_path, 'r').read()
            c = conn.cursor()
            c.execute(cmd)
            conn.commit()
            conn.close()
        except IOError:
            print("Couldn't initialize the database, exiting...")
            raise
        except sqlite3.OperationalError:
            print("Couldn't execute the SQL, exiting...")
            raise
