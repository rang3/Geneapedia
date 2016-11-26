from flask import Flask
from flask import render_template
from flask import request
from flask_mysqldb import MySQL
import MySQLdb
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:cs411fa2016@127.0.0.1/final'
db = SQLAlchemy(app)

class Person(db.Model):
	PID = db.Column(db.Integer)	
	name = db.Column(db.String(60), primary_key=True)
	birth_date = db.Column(db.String(20))
	death_date = db.Column(db.String(20))
	popularity_score = db.Column(db.Integer)

class Child(db.Model):
	child_name = db.Column(db.String(60), primary_key=True)
	parent_name = db.Column(db.String(60), primary_key=True)

class Spouse(db.Model):
	name1 = db.Column(db.String(60), primary_key=True)
	name2 = db.Column(db.String(60), primary_key=True)
	date = db.Column(db.String(20))
	
class Alma_mater(db.Model):
	name = db.Column(db.String(60), primary_key=True)
	university = db.Column(db.String(60), primary_key=True)

# MySQL configurations
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'cs411fa2016'
#app.config['MYSQL_DATABASE_DB'] = 'final'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql = MySQL(app)
#

@app.route('/')
def main():
    return render_template('frontend/index.html')

@app.route('/demo')
def demo():
        return render_template('frontend/demo.html')

@app.route('/aboutus')
def aboutus():
	return render_template('frontend/aboutus.html')

@app.route('/faq')
def faq():
	return render_template('frontend/faq.html')

@app.route('/test')
def test():
	return render_template('frontend/test.html')
	
@app.route('/search', methods=['POST'])
def select():
	#request.form['search']
	spouses = ""
	children = ""
	thePerson = ""
	for (name, spouse) in cursor:
		spouses += "<br/>" + spouse

	cursor.execute("SELECT * FROM (SELECT Person.name, Child.child_name FROM Person INNER JOIN Child ON Person.name=Child.parent_name ORDER BY Person.name) AS C WHERE name=\'%s\';" %(request.form['search']))
	for (name, child) in cursor:
		children += "<br/>" + child
	print spouses
	print children
	cursor.execute("SELECT name FROM Person WHERE name=\'%s\';" %(request.form['search']))
	for name in cursor:
		thePerson += str(name[0])
	return render_template('frontend/demo.html',person=thePerson, spouse=spouses, child=children)

@app.route('/insert', methods=['POST'])
def insertion():
        _name = request.form['name']
        _birth = request.form['birth']
        _death = request.form['death']
        _alma = request.form['almamater']

	
            # All Good, let's call MySQL

	conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
        cursor = conn.cursor()

	if _birth == "":
		_birth='N/A'
	if _death == "":
		_death='N/A'
        cursor.execute('INSERT INTO Person(PID, name,birth_date,death_date,popularity_score) VALUES(0,\'%s\', \'%s\', \'%s\', 0);' %(_name, _birth, _death))

	conn.commit()
        cursor.close()
        conn.close()
	return 'insert done'

@app.route('/delete', methods=['POST'])
def deletion():
        _name = request.form['name']

            # All Good, let's call MySQL

	conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
        cursor = conn.cursor()

	print _name
        cursor.execute('DELETE FROM Person WHERE name=\'%s\'' %(_name))

	conn.commit()
        cursor.close()
        conn.close()
	return 'deleted'

if __name__ == "__main__":
    app.run(port=5002)
