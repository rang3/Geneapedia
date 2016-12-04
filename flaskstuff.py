from flask import Flask
from flask import render_template
from flask import request
from flask_mysqldb import MySQL
import MySQLdb
from flask import jsonify
app = Flask(__name__)

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

@app.route('/searchChild')
def searchChild():
	thePerson = ""
	n = request.args.get('name')
	conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM Person WHERE name=\'%s\';" %n)
	for name in cursor:
		thePerson += str(name[0])
	return thePerson

@app.route('/aboutus')
def aboutus():
	return render_template('frontend/aboutus.html')

@app.route('/faq')
def faq():
	return render_template('frontend/faq.html')

@app.route('/test')
def test():
	return render_template('frontend/test.html')

@app.route('/buildTree', methods=['POST'])
def lookup():
    thisguy = request.args.get('thisguy', '', type=str)
    relation = request.args.get('relation', '', type=str)
    if relation == 'parent':
        return parentOf(thisguy)
    if relation == 'child':
        return childOf(thisguy)
    if relation == 'spouse':
        return spouseOf(thisguy)
    if relation == 'alma':
        return almaOf(thisguy)
    if relation == 'person':
        return infoOf(thisguy)
    if relation == 'popularity':
        return popularityOf(thisguy)

def parentOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    cursor.execute("SELECT Child_final.parent_name FROM Child_final WHERE child_name=\'%s\';" %(thisguy))
    parents = ",".join(cursor)
    return jsonify(result=parents)
    
def childOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    cursor.execute("SELECT Child_final.child_name FROM Child_final WHERE parent_name=\'%s\';" %(thisguy))
    children = ",".join(cursor)
    return jsonify(result=children)

def spouseOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    spouselist = []
    cursor.execute("SELECT Spouse_final.name2 FROM Spouse_final WHERE name1=\'%s\';" %(thisguy))
    for spouse in cursor:
        spouselist.append(spouse)
    cursor.execute("SELECT Spouse_final.name1 FROM Spouse_final WHERE name2=\'%s\';" %(thisguy))
    for spouse in cursor:
        spouselist.append(spouse)
    spouselist = ",".join(spouselist)
    return jsonify(result=spouselist)

def almaOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    cursor.execute("SELECT Alma_mater_final.university FROM Alma_mater_final WHERE name=\'%s\';" %(thisguy))
    schoollist = ",".join(cursor)
    return jsonify(result=schoollist)
    
def infoOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Person_final WHERE name=\'%s\';" %(thisguy))
    attributes = []
    for PID, name, birth_date, death_date, popularity_score in cursor:
        attributes=[PID, name, birth_date, death_date, popularity_score]
    return jsonify(PID=attributes[0], name=attributes[1],birth_date=attributes[2],death_date=attributes[3])

def popularityOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    cursor.execute("SELECT Popularity2.Pscore FROM Popularity2, Person_final WHERE Person_final.PID=Popularity2.PID AND Person_final.name=\'%s\';" %(thisguy))
    theScore = 1
    for score in cursor:
        theScore = str(score[0])
    return jsonify(result=theScore)

@app.route('/search', methods=['POST'])
def select():
	conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
	cursor = conn.cursor()
	print "SELECT * FROM {SELECT Person.name, Spouse.name2 FROM Person INNER JOIN Spouse ON Person.name=Spouse.name1 ORDER BY Person.name} WHERE name=\'%s\';" %(request.form['search'])	

	cursor.execute("SELECT * FROM (SELECT Person.name, Spouse.name2 FROM Person INNER JOIN Spouse ON Person.name=Spouse.name1 ORDER BY Person.name) AS S WHERE name=\'%s\';" %(request.form['search']))
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
