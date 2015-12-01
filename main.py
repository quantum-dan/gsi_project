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
*quiz
	quizzes (id int not null auto_increment primary key, name text)
	questions (id int not null auto_increment primary key, quiz_id int, question text, opt1 text, opt2 text, opt3 text, opt4 text, c_opt int)
"""

@route("/")
def index():
	return template("index.tmpl") 

@route("/quiz")
def quiz_view():
	htString = ""
	questions = getq_html()
	for i in questions:
		htString = htString + ("<form method=POST action='/grade/%s'>%s<br /><input type=submit value='Submit' /></form>" % (i[1], i[0]))
	return template("quiz.tmpl", htString)

@post("/grade/<name>")
def quiz_grade(name):
	questions = [i[6] for i in getq()[name]]
	passed =[(i, int(request.forms.get(str(i)))) for i in questions]
	pct = grade_quiz(name, passed)
	username = request.get_cookie("login", secret=LOGIN_COOKIE_KEY)
	if username:
		insert_score(username, pct)
	return template("graded.tmpl", (pct, name))

@get("/scores")
def view_scores():
	username = request.get_cookie("login", secret=LOGIN_COOKIE_KEY)
	if not username:
		return template("scores.tmpl", "You are not logged in")
	score = avg_score(username)
	return template("scores.tmpl", "Your average score is: %f percent" % score)

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

@post("/create_acct_admin")
def create_account_admin():
	username = request.forms.get("username")
	password = request.forms.get("password1")
	password_check = request.forms.get("password2")
	role = request.forms.get("role")
	user_role = check_role(request.get_cookie("login", secret=LOGIN_COOKIE_KEY))
	if password != password_check:
		return template("base.tmpl", "<p>Passwords do not match.</p>")
	else if user_role == "superuser" or user_role == "admin":
		succeeded = create_account(username, password, role)
		if succeeded:
			return template("admin_panel.tmpl")
		else:
			return template("base.tmpl", "<p>Account with username %s already exists" % username)
	else:
		return template("base.tmpl", "<p>You are not an admin.  Go away.</p>")

@post("/create_quiz")
def create_new_quiz():
	role = check_role(request.get_cookie("login", secret=LOGIN_COOKIE_KEY))
	if role == "admin" or role == "superuser":
		quiz_name = request.forms.get("name")
		create_quiz(quiz_name)
		return template("admin_panel.tmpl")
	else:
		return template("base.tmpl", "<p>You are not an admin.  Go away.</p>")

@post("/add_question")
def add_q_to_quiz():
	role = check_role(request.get_cookie("login", secret=LOGIN_COOKIE_KEY))
	if role == "admin" or role == "superuser":
		quiz_id = int(request.forms.get("id"))
		question = request.forms.get("question")
		opt1 = request.forms.get("opt1")
		opt2 = request.forms.get("opt2")
		opt3 = request.forms.get("opt3")
		opt4 = request.forms.get("opt4")
		c_opt = int(request.forms.get("c_opt"))
		create_question(quiz_id, question, opt1, opt2, opt3, opt4, c_opt)
		return template("admin_panel.tmpl")
	else:
		return template("base.tmpl", "<p>You are not an admin.  Go away.</p>")

@route("/admin")
def admin_panel():
	username = request.get_cookie("login", secret=LOGIN_COOKIE_KEY)
	role = check_role(username)
	if role == "superuser" or role == "admin":
		quizzes = getquizzes()
		htStrings = ["<option value=%s>%s</option" % (i[0], i[1]) for i in quizzes]
		htString = "".join(htStrings)
		return template("admin_panel.tmpl" % htString)
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
