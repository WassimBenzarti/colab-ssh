from flask import Flask, send_file
app = Flask(__name__)

@app.route('/')
def hello_world():
    return send_file("static/index.html")

def launch_api_server(port):
	app.run(port=port)

