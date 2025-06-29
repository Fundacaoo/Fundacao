import json
import os

class Tarefa:
    def __init__(self, id, texto, concluida=False):
        self.id = int(id)
        self.texto = texto
        self.concluida = concluida

    def to_dict(self):
        return {'id': self.id, 'texto': self.texto, 'concluida': self.concluida}

    def marcar_concluida(self):
        self.concluida = True

    def desfazer(self):
        self.concluida = False

    def editar(self, novo_texto):
        self.texto = novo_texto


class PainelEstudos:
    def __init__(self, arquivo_usuario='app/db/tarefas_usuario.json', arquivo_default='app/db/tarefas_default.json'):
        self.arquivo_usuario = arquivo_usuario
        self.arquivo_default = arquivo_default
        self.tarefas = []
        self.inicializar()

    def inicializar(self):
        if not os.path.exists(self.arquivo_usuario) or self._arquivo_vazio_ou_invalido(self.arquivo_usuario):
            print("Criando arquivo do usuário com base nas tarefas default...")
            if os.path.exists(self.arquivo_default):
                with open(self.arquivo_default, 'r', encoding='utf-8') as f:
                    dados_default = json.load(f)
                os.makedirs(os.path.dirname(self.arquivo_usuario), exist_ok=True)
                with open(self.arquivo_usuario, 'w', encoding='utf-8') as f:
                    json.dump(dados_default, f, ensure_ascii=False, indent=4)
        self.carregar()

    def _arquivo_vazio_ou_invalido(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            return not isinstance(dados, list) or len(dados) == 0
        except Exception:
            return True

    def carregar(self):
        if os.path.exists(self.arquivo_usuario):
            try:
                with open(self.arquivo_usuario, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.tarefas = [Tarefa(**d) for d in dados]
            except json.JSONDecodeError:
                self.tarefas = []
        else:
            self.tarefas = []

    def salvar(self):
        with open(self.arquivo_usuario, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self.tarefas], f, ensure_ascii=False, indent=4)

    def adicionar_tarefa(self, texto):
        novo_id = max([t.id for t in self.tarefas], default=0) + 1
        tarefa = Tarefa(novo_id, texto)
        self.tarefas.append(tarefa)
        self.salvar()

    def deletar_tarefa(self, id):
        self.tarefas = [t for t in self.tarefas if t.id != id]
        self.salvar()

    def editar_tarefa(self, id, novo_texto):
        for t in self.tarefas:
            if t.id == id:
                t.editar(novo_texto)
                break
        self.salvar()

    def marcar_concluida(self, id):
        for t in self.tarefas:
            if t.id == id:
                t.marcar_concluida()
                break
        self.salvar()

    def desfazer_concluida(self, id):
        for t in self.tarefas:
            if t.id == id:
                t.desfazer()
                break
        self.salvar()

    def listar_tarefas(self):
        return [t.to_dict() for t in self.tarefas]
