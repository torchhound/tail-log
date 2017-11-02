from flask import Flask, render_template, request, Response
from subprocess import check_output
from functools import wraps

app = Flask(__name__)
app.config.from_pyfile('server.config')

"""Auth snippet(check_auth, authenticate, and requires_auth) copied from http://flask.pocoo.org/snippets/8/"""

def check_auth(username, password):
    """This function is called to check if a username /password combination is valid."""
    return username == WEB_USERNAME and password == WEB_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET"])
@requires_auth
def index():
	"""Returns tail of log"""
	output = check_output('tail -f' + LOG_LOCATION, shell=True)
	return render_template("index.html", output=output)

if __name__ == '__main__':
    app.run()