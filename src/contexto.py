class Contexto:

    def __init__(self, limite_historico=20):
        self.dados = {}
        self.historico = []
        self.limite_historico = limite_historico

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

    def adicionar_historico(self, comando, intencao=None):
        registro = {
            "comando": comando,
            "intencao": intencao
        }

        self.historico.append(registro)

        if len(self.historico) > self.limite_historico:
            self.historico.pop(0)

    def obter_historico(self):
        return self.historico.copy()

    def obter_ultimo_comando(self):
        if not self.historico:
            return None

        return self.historico[-1]

    def limpar_historico(self):
        self.historico.clear()

    def definir_ultima_entidade(self, tipo, identificador):
        self.definir(
            "ultima_entidade",
            {
                "tipo": tipo,
                "identificador": identificador
            }
        )

    def obter_ultima_entidade(self):
        return self.obter("ultima_entidade")

    def limpar_ultima_entidade(self):
        self.remover("ultima_entidade")