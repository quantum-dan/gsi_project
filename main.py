from bottle import route, run, get, post, request, static_file, error, response

def template(filename, args=()):
	f = open("templates/" + filename, "r")
	fstring = f.read()
	f.close()
	return fstring % args

@route("/")
def index():
	return template("index.tmpl") 

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

def check_login(username, password):
	if username == "Daniel":
		return True
	else:
		return False

@post("/login")
def do_login():
	username = request.forms.get("username")
	password = request.forms.get("password")
	if check_login(username, password):
		response.set_cookie("login", username, secret="user_logged_in")
		return template("logged_in.tmpl", username)
	else:
		return template("log_in.tmpl", "Login failed.")

@get("/login")
def login():
	username = request.get_cookie("login", secret="user_logged_in")
	if username:
		return template("logged_in.tmpl", username)
	else:
		return template("log_in.tmpl", "You are not logged in.")

run(host="0.0.0.0", port=8000, debug=True)
