from config import db
from blueprints.users import users
from ldap3.utils.hashed import hashed
from blueprints.bluedocker import bdocker
from ldap3 import Server, Connection, HASHED_MD5
from flask import Flask, render_template, flash, redirect, request, jsonify, session

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(bdocker)
app.secret_key = 'flask-app'

server = Server('ldap://127.0.0.1:389')
DN = 'cn=admin,dc=dexter,dc=com,dc=br'

@app.route('/')
def index():
    if 'auth' in session:
        return redirect('/users')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    dn = 'mail={0},dc=dexter,dc=com,dc=br'.format(data['email'])
    ldap = Connection(server, dn, data['senha'])
    if ldap.bind():
        session['auth'] = True
        return redirect('/users')
    else:
        flash('Usuário ou senha inválidos. Tente novamente.', 'danger')
        return redirect('/')

@app.route('/logoff', methods=['GET'])
def logoff():
    if 'auth' in session:
        del session['auth']
    return redirect('/')

@app.route('/jenkins')
def jenkins():
    return render_template('jenkins.html')

app.run(host='0.0.0.0',port=80, debug=True)