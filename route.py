from app.controllers.application import Application
from bottle import Bottle, route, run, static_file

app = Bottle()
ctl = Application()

#-----------------------------------------------------------------------------
# Rotas estáticas

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

#-----------------------------------------------------------------------------
# Rotas principais

@app.route('/')
def home():
    return ctl.render('index')

@app.route('/index')
def action_pagina():
    return ctl.render('index')

@app.route('/login', method='POST')
def process_login():
    return ctl.handle_login()

@app.route('/cadastro', method='POST')
def process_cadastro():
    return ctl.handle_cadastro()

@app.route('/users', method='GET')
def api_get_all_users():
    return ctl.get_all_users()

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
