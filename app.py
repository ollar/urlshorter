from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
import datetime


app = Flask(__name__)
app.secret_key = b'<A;\xad\xa2\x0e\xac\x0eY\x80'


@app.before_request
def connect_db():
    g.sqlite_db = sqlite3.connect('example.db')
    g.db_cursor = g.sqlite_db.cursor()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        g.db_cursor.execute("select * from urls")

        urls = g.db_cursor.fetchall()

        return render_template('index.html', urls=urls)

    elif request.method == 'POST':
        if not request.form.get('normal_url') or not request.form.get('alias'):
            flash('Incorrect data', 'error')
            return redirect(url_for('main'))
        try:
            # # Insert a row of data
            g.db_cursor.execute("""INSERT INTO urls (
                    normal_url,
                    alias,
                    timestamp,
                    ip
                ) VALUES (?,?,?,?)""", (
                    request.form.get('normal_url'),
                    request.form.get('alias'),
                    str(datetime.datetime.now()),
                    request.remote_addr)
                )
            g.sqlite_db.commit()

        except sqlite3.IntegrityError:
            flash('Such alias already exists', 'error')
            return redirect(url_for('main'))

        flash('Url added successfully')

        return redirect(url_for('main'))


@app.route('/remove_url', methods=['GET'])
def remove_url():
    g.db_cursor.execute("delete from urls where id=?",
                        (request.args.get('urlid'),)
                        )

    g.sqlite_db.commit()
    flash('Url removed successfully')

    return redirect(url_for('main'))


@app.route('/<string:alias>')
def go_to_url(alias):
    g.db_cursor.execute("select * from urls where alias=?", (alias,))

    entry = g.db_cursor.fetchone()

    if (entry):
        url = entry[1]
        redirect_url = ''

        try:
            url.index('http://')
            url.index('https://')
            redirect_url = url
        except ValueError:
            redirect_url = 'http://' + url

        return redirect(redirect_url)

    else:
        flash('No such alias, sorry', 'error')
        return redirect(url_for('main'))


if __name__ == '__main__':
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists urls
                 (id integer primary key, normal_url text,
                 alias text unique, timestamp text, ip text)''')

    conn.commit()
    conn.close()

    app.run('0.0.0.0', 8000, debug=True)
