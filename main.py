from bottle import route, run

def template(filename, args=()):
	f = open("templates/" + filename, "r")
	fstring = f.read()
	f.close()
	return fstring % args

@route("/")
def index():
	return template("index.tmpl") 

run(host="0.0.0.0", port=8000, debug=True)
