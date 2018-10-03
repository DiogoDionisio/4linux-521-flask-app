import logging
from functools import wraps
from pymongo import MongoClient
from configparser import ConfigParser
from flask import redirect, session, request

config = ConfigParser()
config.read('config.ini')

client = MongoClient(config['db']['host'])
db = client[config['db']['base']]

logging.basicConfig(filename='app.log', datefmt='%d/%m/%Y %H:%M:%S', level=logging.WARNING, 
format='%(asctime)s [%(levelname)s]: %(filename)s line %(lineno)s on %(funcName)s: %(message)s')

def auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'auth' not in session:
            logging.warning('Usuário não autenticado acessando {0}'.format(request.path))
            return redirect('/')
        logging.warning('Usuário autenticado acessando {0}'.format(request.path))
        return f(*args, **kwargs)
    return decorated