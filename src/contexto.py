class Contexto:

    def __init__(self):
        self.dados = {}

    def definir(self, chave, valor):
        self.dados[chave] = valor

    def obter(self, chave, padrao=None):
        return self.dados.get(chave, padrao)

    def remover(self, chave):
        self.dados.pop(chave, None)

    def limpar(self):
        self.dados.clear()

    def existe(self, chave):
        return chave in self.dados

    def mostrar(self):
        return self.dados.copy()