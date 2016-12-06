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

@app.route('/test2')
def test():
    return render_template('frontend/test2.html')

@app.route('/buildTree', methods=['GET'])
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
    cursor.execute("SELECT count(*)  FROM Child_final2 WHERE child_name=\'%s\';" %(thisguy))
    length = cursor.fetchone()[0]
    cursor.execute("SELECT Child_final2.parent_name FROM Child_final2 WHERE child_name=\'%s\';" %(thisguy))
    parents = []
    for i in range(length):
        parents.append(cursor.fetchone()[0])
    parents = ",".join(parents)
    print(parents)
    return jsonify(result=parents)
    
def childOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM Child_final2 WHERE parent_name=\'%s\';" %(thisguy))
    length = cursor.fetchone()[0]
    cursor.execute("SELECT Child_final2.child_name FROM Child_final2 WHERE parent_name=\'%s\';" %(thisguy))
    children = []
    for i in range(length):
        children.append(cursor.fetchone()[0])
    children = ",".join(children)
    print(children)
    return jsonify(result=children)

def spouseOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM Spouse_final2 WHERE name2=\'%s\';" %(thisguy))
    length = cursor.fetchone()[0]
    cursor.execute("SELECT Spouse_final2.name1 FROM Spouse_final2 WHERE name2=\'%s\';" %(thisguy))
    spouselist = []
    for i in range(length):
        spouselist.append(cursor.fetchone()[0])
    spouselist = ",".join(spouselist)
    print(spouselist)
    return jsonify(result=spouselist)

def almaOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM Alma_mater_final2 WHERE name=\'%s\';" %(thisguy))
    length = cursor.fetchone()[0]
    cursor.execute("SELECT Alma_mater_final2.university FROM Alma_mater_final2 WHERE name=\'%s\';" %(thisguy))
    schoollist=[]
    for i in range(length):
        schoollist.append(cursor.fetchone()[0])
    schoollist = ",".join(schoollist)
    return jsonify(result=schoollist)
    
def infoOf(thisguy):
    conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Person_final2 WHERE name=\'%s\';" %(thisguy))
    attributes = []
    for PID, name, birth_date, death_date, popularity_score in cursor:
        attributes=[PID, name, birth_date, death_date, popularity_score]
    return jsonify(PID=attributes[0], name=attributes[1],birth_date=attributes[2],death_date=attributes[3])

@app.route('/search', methods=['POST'])
def select():
	conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
	cursor = conn.cursor()
	print "SELECT * FROM {SELECT Person_final2.name, Spouse_final2.name2 FROM Person_final2 INNER JOIN Spouse_final2 ON Person_final2.name=Spouse_final2.name1 ORDER BY Person_final2.name} WHERE name=\'%s\';" %(request.form['search'])	

	cursor.execute("SELECT * FROM (SELECT Person_final2.name, Spouse_final2.name2 FROM Person_final2 INNER JOIN Spouse_final2 ON Person_final2.name=Spouse_final2.name1 ORDER BY Person_final2.name) AS S WHERE name=\'%s\';" %(request.form['search']))
	spouses = ""
	children = ""
	thePerson = ""
	for (name, spouse) in cursor:
		spouses += "<br/>" + spouse

	cursor.execute("SELECT * FROM (SELECT Person_final2.name, Child_final2.child_name FROM Person_final2 INNER JOIN Child_final2 ON Person_final2.name=Child_final2.parent_name ORDER BY Person_final2.name) AS C WHERE name=\'%s\';" %(request.form['search']))
	for (name, child) in cursor:
		children += "<br/>" + child
	print spouses
	print children
	cursor.execute("SELECT name FROM Person_final2 WHERE name=\'%s\';" %(request.form['search']))
	for name in cursor:
		thePerson += str(name[0])
	return render_template('frontend/demo.html',person=thePerson, spouse=spouses, child=children)

@app.route('/insert', methods=['POST'])
def insertion():
        _name = request.form['name']
        _birth = request.form['birth']
        _death = request.form['death']
        _alma = request.form['almamater']
        _children = request.form['children']
        _parent = request.form['parent']
        _spouse = request.form['spouse']
	
            # All Good, let's call MySQL

	conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
        cursor = conn.cursor()

	if _birth == "":
		_birth='N/A'
	if _death == "":
		_death='N/A'
        cursor.execute('INSERT INTO Person_final2(PID, name,birth_date,death_date,popularity_score) VALUES(0,\'%s\', \'%s\', \'%s\', 50);' %(_name, _birth, _death))
    if _child != "":
        childlist = _child.strip().split(',');
        for c in childlist:
            if c != "":
                cursor.execute('INSERT INTO Child_final2(child_name, parent_name) VALUES(\'%s\', \'%s\');' %(c, _name))
    if _parent != "":
        parentlist = _parent.strip().split(',');
        for p in parentlist:
            if p != "":
                cursor.execute('INSERT INTO Child_final2(child_name, parent_name) VALUES(\'%s\', \'%s\');' %(_name, p))

    if _spouse != "":
        spouselist = _spouse.strip().split(',');
        for s in spouselist:
            if s != "":
                cursor.execute('INSERT INTO Spouse_final2(name1, name2) VALUES(\'%s\', \'%s\');' %(_name, s))


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
        cursor.execute('DELETE FROM Person_final2 WHERE name=\'%s\'' %(_name))

	conn.commit()
        cursor.close()
        conn.close()
	return 'deleted'

if __name__ == "__main__":
    app.run(port=5002)
