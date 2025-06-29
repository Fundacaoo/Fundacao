from app.controllers.package.application import Application
from app.controllers.package.painel import PainelEstudos  
from bottle import Bottle, request, response, run, static_file
import json

app = Bottle()
ctl = Application()
painel = PainelEstudos()

# -----------------------------------------------------------------------------
# Rotas estáticas

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# Rotas do Painel de Estudos

@app.get('/tarefas')
def listar():
    response.content_type = 'application/json'
    return json.dumps(painel.listar_tarefas(), ensure_ascii=False)

@app.post('/tarefas')
def adicionar():
    data = request.json
    texto = data.get('texto')
    if texto:
        painel.adicionar_tarefa(texto)
        return {'mensagem': 'Tarefa adicionada'}
    response.status = 400
    return {'erro': 'Texto é obrigatório'}

@app.delete('/tarefas/<id:int>')
def deletar(id):
    painel.deletar_tarefa(id)
    return {'mensagem': 'Tarefa deletada'}

@app.put('/tarefas/<id:int>')
def editar(id):
    data = request.json
    novo_texto = data.get('texto')
    if novo_texto:
        painel.editar_tarefa(id, novo_texto)
        return {'mensagem': 'Tarefa editada'}
    response.status = 400
    return {'erro': 'Texto é obrigatório'}

@app.patch('/tarefas/<id:int>/concluir')
def concluir(id):
    painel.marcar_concluida(id)
    return {'mensagem': 'Tarefa concluída'}

@app.patch('/tarefas/<id:int>/desfazer')
def desfazer(id):
    painel.desfazer_concluida(id)
    return {'mensagem': 'Conclusão desfeita'}

# -----------------------------------------------------------------------------
# Executar

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)
