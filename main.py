from flask import flash, request, make_response, redirect, render_template, session
import unittest

from app import create_app
from app.forms import LoginForm


app = create_app()

app.config['SECRET_KEY'] = 'SUPER SECRETO'

todos = ['☕', '🍌', '🐟']

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def not_found(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
def hello_world():
    user_ip = session.get('user_ip')
    loginForm = LoginForm()
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': loginForm,
        'username': username,
    }

    if loginForm.validate_on_submit():
        username = loginForm.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con éxito')

        return make_response(redirect('/hello'))

    return render_template('hello.html', **context)

if __name__ == '__main__':
    app.run(debug=True)