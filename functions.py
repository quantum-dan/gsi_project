from bottle import route, run, get, post, request, response
import pymysql
from conf import *

"""
database structure
*users
	users (id int, login text, password text, role text)
*quiz
	quizzes (id int, name text)
	questions (id int, quiz_id int, question text, opt1 text, opt2 text, opt3 text, opt4 text, c_opt int)
"""

def getquizzes():
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="quiz")
	c = conn.cursor()
	c.execute("SELECT id, name FROM quizzes")
	quizzes = [(i[0], unsanitize(i[1])) for i in c]
	c.close()
	conn.close()
	return quizzes

def getq():
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="quiz")
	c = conn.cursor()
	c.execute("SELECT id, name FROM quizzes")
	quizzes = [(i[0], unsanitize(i[1])) for i in c]
	questions = {}
	for i in quizzes:
		name = i[1]
		id = int(i[0])
		c.execute("SELECT id, question, opt1, opt2, opt3, opt4, c_opt FROM questions WHERE quiz_id=%d" % id)
		questions[name] = [[ unsanitize(x[1]), unsanitize(x[2]), unsanitize(x[3]), unsanitize(x[4]), unsanitize(x[5]), x[6], x[0] ] for x in c]
	c.close()
	conn.close()
	return questions

def create_quiz(name):
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="quiz")
	c = conn.cursor()
	c.execute("INSERT INTO quizzes (name) VALUES ('%s')" % sql_sanitize(name))
	c.close()
	conn.commit()
	conn.close()

def create_question(quiz_id, question, opt1, opt2, opt3, opt4, c_opt):
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="quiz")
	c = conn.cursor()
	c.execute("INSERT INTO questions (quiz_id, question, opt1, opt2, opt3, opt4, c_opt) VALUES (%d, '%s', '%s', '%s', '%s', '%s', %d)" % (int(quiz_id), sql_sanitize(question), sql_sanitize(opt1), sql_sanitize(opt2), sql_sanitize(opt3), sql_sanitize(opt4), int(c_opt)))
	c.close()
	conn.commit()
	conn.close()

def insert_score(user, score):
	user = sql_sanitize(user)
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="users")
	c = conn.cursor()
	c.execute("INSERT INTO scores (username, score) VALUES ('%s', %f)" % (user, score))
	conn.commit()
	c.close()
	conn.close()

def get_scores(user):
	user = sql_sanitize(user)
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="users")
	c = conn.cursor()
	c.execute("SELECT score FROM scores WHERE username='%s'" % user)
	scores = []
	for row in c:
		scores.append(float(row[0]))
	c.close()
	conn.close()
	return scores

def avg_score(user):
	scores = get_scores(user)
	if len(scores) == 0:
		return 0.0
	else:
		return sum(scores)/float(len(scores))

def getq_html():
	questions = getq()
	htStrings = []
	for i in questions:
		question = questions[i]
		htString = "<input type=radio name='%s' value=%d>%s</input><br />"
		htStrings.append((("<h5>%s</h5>" % i) +  "".join([("<h6>%s</h6>" % q[0]) + "".join([htString % (q[6], n-1, q[n]) for n in range(1, 5)]) for q in question]), i))
	return htStrings

def grade_quiz(quiz, questions):
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="quiz")
	c = conn.cursor()
	c.execute("SELECT id FROM quizzes WHERE name='%s'" % sql_sanitize(quiz))
	id = 0
	for row in c:
		id = int(row[0])
		break
	c.execute("SELECT question, c_opt, id FROM questions WHERE quiz_id=%d" % id)
	questions_db = {}
	questions_n = 0
	for row in c:
		questions_db[row[2]] = row[1]
		questions_n += 1
	c.close()
	conn.close()
	total = 0
	for q in questions:
		question = questions_db[q[0]]
		if q[1] == question:
			total += 1
	return 100 * float(total)/float(questions_n)

def template(filename, args=()):
	f = open("templates/" + filename, "r")
	fstring = f.read()
	f.close()
	return fstring % args

def sql_sanitize(string):
	vals = [ord(i) for i in string]
	vals = [str(i) for i in vals]
	result = " ".join(vals)
	return result

def unsanitize(string):
	vals = string.split(" ")
	vals = [int(i) for i in vals if i != " "]
	vals = [chr(i) for i in vals]
	result = "".join(vals)
	return result

def create_account(username, password, role):
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="users")
	c = conn.cursor()
	found = False
	result = False
	c.execute("SELECT login FROM users WHERE login='%s'" % sql_sanitize(username))
	for row in c:
		found = True
	if not found:
		c.execute("INSERT INTO users (login, password, role) VALUES ('%s', '%s', '%s')" % (sql_sanitize(username), sql_sanitize(password), sql_sanitize(role)))
		result = True
		c.close()
		conn.commit()
		conn.close()
	return result

def check_login(username, password):
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="users")
	c = conn.cursor()
	username = sql_sanitize(username)
	password = sql_sanitize(password)
	c.execute("SELECT password FROM users WHERE login='%s'" % username)
	result = False
	for row in c:
		if row[0] == password:
			result = True
			break
	c.close()
	conn.close()
	return result

def check_role(username):
	conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="users")
	c = conn.cursor()
	c.execute("SELECT role FROM users WHERE login='%s'" % sql_sanitize(username))
	result = ""
	for row in c:
		result = unsanitize(row[0])
	c.close()
	conn.close()
	return result
