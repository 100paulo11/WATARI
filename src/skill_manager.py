from src.skills.sistema import mostrar_informacoes_sistema
from src.skills.processos import listar_processos
from src.skills.aplicativos import abrir, fechar


class SkillManager:

    def __init__(self):
        self.skills = {}

        self.registrar_skill(
            "SISTEMA",
            self._executar_sistema
        )

        self.registrar_skill(
            "PROCESSOS",
            self._executar_processos
        )

        self.registrar_skill(
            "APLICATIVOS",
            self._executar_aplicativos
        )

    def registrar_skill(self, nome, funcao):
        nome = nome.upper()

        self.skills[nome] = funcao

    def listar_skills(self):
        return list(self.skills.keys())

    def executar(self, skill, comando=None):

        skill = skill.upper()

        if skill not in self.skills:
            print(f"Watari: A Skill '{skill}' não existe.")
            return

        funcao = self.skills[skill]

        funcao(comando)

    def _executar_sistema(self, comando=None):
        mostrar_informacoes_sistema()

    def _executar_processos(self, comando=None):
        listar_processos()

    def _executar_aplicativos(self, comando=None):

        if comando is None:
            return

        acao = comando.get("acao")
        aplicativo = comando.get("aplicativo")

        if acao == "ABRIR":
            abrir(aplicativo)

        elif acao == "FECHAR":
            fechar(aplicativo)