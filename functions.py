from bottle import route, run, get, post, request, response
import pymysql
from conf import *

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
