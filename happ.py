#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from os import path

from flask import Flask, redirect, request, session, escape, url_for, send_from_directory
from jinja2 import select_autoescape, ChoiceLoader, FileSystemLoader, Environment

from classes.pharrell import Pharrell


# from https://github.com/lfdebrux/govuk-frontend-python/blob/d3dd9f6cb689731753346746d2b5c7229f5293e2/govuk_frontend/templates.py#L12
class Environment2(Environment):
    def join_path(self, template, parent):
        """Enable the use of relative paths in template import statements"""
        return path.normpath(path.join(path.dirname(parent), template))

app = Flask(__name__)
env = Environment2(loader=ChoiceLoader([FileSystemLoader('templates/'),
                                        FileSystemLoader("node_modules/govuk-frontend/"),
                                        FileSystemLoader("node_modules/govuk-frontend/components/")]),
                  autoescape=select_autoescape(['html', 'xml']),
                  extensions=[])

app.secret_key = b'dmVyeXZlcnl2ZXJ5c2VjdXJl'


@app.route('/', methods=['GET'])
@app.route('/<path>', methods=['GET'])
def hello_world(path=''):

    if path == 'redirect':
        return redirect('/youve_been_redirected')

    template = env.get_template('index.html')
    return template.render(path=path, message=Pharrell().get_message())


@app.route('/teams/gds/delivery-and-support/technology-operations', methods=['GET'])
def techops_team():
    template = env.get_template('techops.html')
    return template.render()


@app.route('/teams/gds/delivery-and-support/technology-operations/traceability', methods=['GET'])
def traceability_team():
    template = env.get_template('traceability.html')
    return template.render()


@app.route('/teams/gds/delivery-and-support/technology-operations/cyber', methods=['GET'])
def cyber_team():
    template = env.get_template('cyber.html')
    return template.render()

@app.route('/teams/gds/delivery-and-support/technology-operations/cyber/tooling', methods=['GET'])
def cyber_tooling_team():
    with open('data/CT.json') as f:
        data = json.load(f)

    template = env.get_template('cyber-tooling.html')
    return template.render(metrics=data)


@app.route('/teams/gds/delivery-and-support/technology-operations/reliability-engineering', methods=['GET'])
def re_team():
    template = env.get_template('reliability-engineering.html')
    return template.render()


@app.route('/teams/gds/delivery-and-support/technology-operations/reliability-engineering/paas', methods=['GET'])
def paas_team():
    with open('data/paas.json') as f:
        data = json.load(f)

    template = env.get_template('paas.html')
    return template.render(metrics=data)


@app.errorhandler(404)
def fourohfour(error):
    return '404!', 404


@app.route('/secure', methods=['GET', 'POST'])
def access_secure_area():
    if 'username' in session:
        return '''
                <h2>Logged in as '{}'</h2>
                <a href="{}">Logout</a>
            '''.format(escape(session['username']), url_for('logout'))
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('access_secure_area'))
    return '''
        <form method="POST">
            <p><input type="text" name="username">
            <p><input type="submit" value="Login">
        </form>
    '''


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('hello_world'))


# load assets directly from govuk-frontend package
# this is done instead of overriding the `static` directory in Flask()
@app.route('/assets/<path:filename>')
def send_file(filename):
    return send_from_directory('node_modules/govuk-frontend/assets/', filename)


#if __name__ == '__main__':
#    app.run()
