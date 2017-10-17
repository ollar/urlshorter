from app import app
import sqlite3
import os

if not os.path.exists('urls.db'):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE if not exists urls
                 (id integer primary key, normal_url text,
                 alias text unique, timestamp text, ip text)""")

    conn.commit()
    conn.close()

    app.run()
