app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/demo')
def insertion():
        _name = request.form['name']
        _birth = request.form['birth']
        _death = request.form['death']
        _nationality = request.form['nationality']

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()

        cursor.execute('insertUser', _name, _birth, _death, _nationality) # insert

        cursor.close()
        conn.close()

def deletion():
        _name = request.form['name']

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()

        cursor.callproc('deleteUser', (_name))

        cursor.close()
        conn.close()

def search():
        _name = request.form['name']

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute('search', (_name))

        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(port=5002)
