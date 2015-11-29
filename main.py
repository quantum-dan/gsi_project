from bottle import route, run, get, post, request, static_file, error, response
import pymysql
from conf import *
from functions import *

"""PyMySQL Directions:
conn = pymysql.connect(host="localhost", port=3306, user=DEFAULT_MYSQL, passwd=MYSQL_PASSWORDS[DEFAULT_MYSQL], db="dbname")
cur = conn.cursor()
cur.execute("insert stuff, etc")
cur.execute("select stuff")
for row in cur:
	print(row)
cur.close()
conn.close()"""

"""Database Structure:
*users
	users (id int not null auto_increment primary key, login text, password text, role text)
"""

@route("/")
def index():
	return template("index.tmpl") 

@get("/create_acct")
def create_acct():
	return template("create_acct.tmpl", "Create an account")

@post("/create_acct")
def create_account_post():
	username = request.forms.get("username")
	password = request.forms.get("password1")
	password_check = request.forms.get("password2")
	role = "user"
	if password != password_check:
		return template("create_acct.tmpl", "Passwords do not match")
	else:
		succeeded = create_account(username, password, role)
		if succeeded:
			return template("create_acct.tmpl", "Successfully created account with username %s" % username)
		else:
			return template("create_acct.tmpl", "Account with username %s already exists" % username)

@route("/admin")
def admin_panel():
	username = request.get_cookie("login", secret=LOGIN_COOKIE_KEY)
	role = check_role(username)
	if role == "superuser" or role == "admin":
		return template("admin_panel.tmpl")
	return template("not_admin.tmpl")

@route("/<user>")
def uview(user="None"):
	return template("user.tmpl", user)

@get("/post")
def post_get():
	return template("post.tmpl", "You have not sent a POST request")

@post("/post")
def post_post():
	return template("post.tmpl", request.forms.get("content")) 

@route("/static/<filename>")
def serve_static(filename):
	return static_file(filename, root="/home/freebsd/py/server/static")

@error(404)
def error404(error):
	return template("error404.tmpl")

@post("/login")
def do_login():
	username = request.forms.get("username")
	password = request.forms.get("password")
	if check_login(username, password):
		response.set_cookie("login", username, secret=LOGIN_COOKIE_KEY)
		return template("logged_in.tmpl", username)
	else:
		return template("log_in.tmpl", "Login failed.")

@get("/login")
def login():
	username = request.get_cookie("login", secret=LOGIN_COOKIE_KEY)
	if username:
		return template("logged_in.tmpl", username)
	else:
		return template("log_in.tmpl", "You are not logged in.")

run(host="0.0.0.0", port=8000, debug=True)
