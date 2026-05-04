from flask import Flask, request

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
	return response


@app.route('/health', methods=['GET', 'OPTIONS'])
def index():
	# Respond to CORS preflight
	if request.method == 'OPTIONS':
		return "", 200
	return "OK"


if __name__ == '__main__':
	# Bind to all interfaces on port 8080
	app.run(host='0.0.0.0', port=8080, debug=True)
