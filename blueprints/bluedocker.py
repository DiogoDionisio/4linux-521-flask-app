from config import db
from docker import DockerClient
from bson.objectid import ObjectId
from flask import Blueprint, render_template, flash, redirect, request

dc = DockerClient('tcp://127.0.0.1:2376')

bdocker = Blueprint('bdocker', __name__)

@bdocker.route('/docker')
def index_docker():
	for container in dc.containers.list(all=True):
		if container.name == 'flask-app':
			c = container
			break
	else:
		c = {'name' : '-', 'short_id' : '-', 'image' : {'tags' : ['-']}}
	return render_template('docker.html', c=c)

@bdocker.route('/docker/start')
def start_docker():
	for c in dc.containers.list(all=True):
		if c.name == 'flask-app':
			c.start()
			break
	else:
		dc.containers.run('python:alpine', 'sh', name='flask-app', detach=True, tty=True)
	flash('O container flask-app foi iniciado com sucesso!')
	return redirect('/docker')

@bdocker.route('/docker/stop/<cid>')
def stop_docker(cid):
	for c in dc.containers.list():
		if c.short_id == cid:
			c.stop()
			break
	flash('O container flask-app foi parado com sucesso!')
	return redirect('/docker')