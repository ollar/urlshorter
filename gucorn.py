from main.app import app

if __name__ == "__main__":
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE if not exists urls
                 (id integer primary key, normal_url text,
                 alias text unique, timestamp text, ip text)""")

    conn.commit()
    conn.close()

    app.run()
