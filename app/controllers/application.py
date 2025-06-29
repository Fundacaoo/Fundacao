import json
import os
import bcrypt
from bottle import request, redirect, template, response

class Application():
    def __init__(self):
        self.pages = {
            'index': self.index,
        }
        self.users_file = 'app/db/users.json'

        # Garante que a pasta exista
        data_dir = os.path.dirname(self.users_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Garante que o arquivo exista
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump([], f)

    def render(self, page):
        content = self.pages.get(page, self.helper)
        return content()

    def helper(self):
        return template('app/views/html/helper')
    
    def index(self):
        return template('app/views/html/index')

    def handle_cadastro(self):
        nome = request.forms.get('nome')
        email = request.forms.get('email')
        password = request.forms.get('password')

        if not (nome and email and password):
            response.status = 400
            return "Dados incompletos!"

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        # Checa se email já existe
        for user in users:
            if user['email'] == email:
                return "Email já cadastrado!"

        # Gerar hash da senha
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Adiciona novo usuário
        users.append({
            'nome': nome,
            'email': email,
            'password': hashed_pw
        })

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        redirect('/?cadastro=sucesso')

    def handle_login(self):
        email = request.forms.get('email')
        password = request.forms.get('password')

        if not (email and password):
            response.status = 400
            return "Dados incompletos!"

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        # Verifica se existe
        for user in users:
            if user['email'] == email:
                # Verifica hash da senha
                hashed_pw = user['password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
                    nome_usuario = user['nome']
                    return template('app/views/html/aluno', nome_usuario=nome_usuario)

        return "Login inválido!"

    def get_all_users(self):
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        response.content_type = 'application/json'
        return json.dumps(users, indent=4)
