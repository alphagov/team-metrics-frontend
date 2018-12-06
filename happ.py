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

base_breadcrumbs = [ { 'link': '#', 'name': 'GDS' },
                    { 'link': '#', 'name': 'Delivery & Support' },
                    ]
techops_breadcrumbs = base_breadcrumbs.copy()
techops_breadcrumbs.append({ 'link': '/teams/gds/delivery-and-support/technology-operations', 'name': 'Technology Operations' })
cyber_breadcrumbs = techops_breadcrumbs.copy()
cyber_breadcrumbs.append({ 'link': '/teams/gds/delivery-and-support/technology-operations/cyber', 'name': 'Cyber' })
re_breadcrumbs = techops_breadcrumbs.copy()
re_breadcrumbs.append({ 'link': '/teams/gds/delivery-and-support/technology-operations/reliability-engineering', 'name': 'Reliability Engineering' })

@app.route('/teams/gds/delivery-and-support/technology-operations', methods=['GET'])
def techops_team():
    with open('data/dummy.json') as f:
        data = json.load(f)

    template = env.get_template('team-view.html')
    team = {'name': 'Technology Operations', 'details': 'something something Technology Operations', 'has_subteams': 'true' }
    breadcrumbs = techops_breadcrumbs.copy()
    subteams = [ { 'has_subteams': 'true', 'link': '/teams/gds/delivery-and-support/technology-operations/reliability-engineering', 'name': 'Reliability Engineering' },
                 { 'has_subteams': 'true', 'link': '#', 'name': 'User Support' },
                 { 'has_subteams': 'true', 'link': '/teams/gds/delivery-and-support/technology-operations/cyber', 'name': 'Cyber Security' },
                 { 'has_subteams': 'false', 'link': '/teams/gds/delivery-and-support/technology-operations/traceability', 'name': 'Traceability' },
                 { 'has_subteams': 'false', 'link': '#', 'name': 'TechOps Homepage' },
                 ]
    return template.render(team=team, breadcrumbs=breadcrumbs, subteams=subteams, metrics=data)


@app.route('/teams/gds/delivery-and-support/technology-operations/traceability', methods=['GET'])
def traceability_team():
    with open('data/dummy.json') as f:
        data = json.load(f)

    template = env.get_template('team-view.html')
    team = {'name': 'Traceability', 'details': 'something something Traceability', 'has_subteams': 'false' }
    breadcrumbs = techops_breadcrumbs.copy()
    breadcrumbs.append({ 'link': '/teams/gds/delivery-and-support/technology-operations/traceability', 'name': team['name'] })
    return template.render(team=team, breadcrumbs=breadcrumbs, subteams=[], metrics=data)


@app.route('/teams/gds/delivery-and-support/technology-operations/cyber', methods=['GET'])
def cyber_team():
    with open('data/dummy.json') as f:
        data = json.load(f)

    template = env.get_template('team-view.html')
    team = {'name': 'Cyber', 'details': 'something something Cyber', 'has_subteams': 'true' }
    breadcrumbs = cyber_breadcrumbs.copy()
    subteams = [ { 'has_subteams': 'false', 'link': '#', 'name': 'Engage' },
                 { 'has_subteams': 'false', 'link': '/teams/gds/delivery-and-support/technology-operations/cyber/tooling', 'name': 'Tooling' },
                 { 'has_subteams': 'false', 'link': '#', 'name': 'Operational Intelligence' },
                 { 'has_subteams': 'false', 'link': '#', 'name': 'Consult' },
                 ]
    return template.render(team=team, breadcrumbs=breadcrumbs, subteams=subteams, metrics=data)

@app.route('/teams/gds/delivery-and-support/technology-operations/cyber/tooling', methods=['GET'])
def cyber_tooling_team():
    with open('data/CT.json') as f:
        data = json.load(f)

    template = env.get_template('team-view.html')
    team = {'name': 'Tooling', 'details': 'something something Cyber Tooling', 'has_subteams': 'false' }
    breadcrumbs = cyber_breadcrumbs.copy()
    breadcrumbs.append({ 'link': '/teams/gds/delivery-and-support/technology-operations/cyber/tooling', 'name': team['name'] })
    return template.render(team=team, breadcrumbs=breadcrumbs, subteams=[], metrics=data)


@app.route('/teams/gds/delivery-and-support/technology-operations/reliability-engineering', methods=['GET'])
def re_team():
    with open('data/dummy.json') as f:
        data = json.load(f)

    template = env.get_template('team-view.html')
    team = {'name': 'Reliability Engineering', 'details': 'something something Reliability Engineering', 'has_subteams': 'true' }
    breadcrumbs = re_breadcrumbs.copy()
    subteams = [ { 'has_subteams': 'false', 'link': '#', 'name': 'New Platform - Build' },
                 { 'has_subteams': 'false', 'link': '#', 'name': 'New Platform - Run' },
                 { 'has_subteams': 'false', 'link': '#', 'name': 'New Platform - Observe' },
                 { 'has_subteams': 'false', 'link': '/teams/gds/delivery-and-support/technology-operations/reliability-engineering/paas', 'name': 'GOV.UK PaaS' },
                 { 'has_subteams': 'false', 'link': '#', 'name': 'GOV.UK Migration' },
                 { 'has_subteams': 'false', 'link': '#', 'name': 'Automate' },
                 ]
    return template.render(team=team, breadcrumbs=breadcrumbs, subteams=subteams, metrics=data)


@app.route('/teams/gds/delivery-and-support/technology-operations/reliability-engineering/paas', methods=['GET'])
def paas_team():
    with open('data/paas.json') as f:
        data = json.load(f)

    template = env.get_template('team-view.html')
    team = {'name': 'GOV.UK PaaS', 'details': 'something something GOV.UK PaaS', 'has_subteams': 'false' }
    breadcrumbs = re_breadcrumbs.copy()
    breadcrumbs.append({ 'link': '/teams/gds/delivery-and-support/technology-operations/reliability-engineering/paas', 'name': team['name'] })
    return template.render(team=team, breadcrumbs=breadcrumbs, subteams=[], metrics=data)


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
