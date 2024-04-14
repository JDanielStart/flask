from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    user_ip = request.remote_addr

    return f'Hello World! Your IP is {user_ip}'

if __name__ == '__main__':
    app.run(debug=True)