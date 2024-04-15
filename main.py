from flask import Flask, flash, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRETO'

todos = ['☕', '🍌', '🐟']

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Enviar')

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