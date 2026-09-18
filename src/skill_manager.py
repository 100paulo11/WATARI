from src.skills.sistema import mostrar_informacoes_sistema
from src.skills.processos import listar_processos


class SkillManager:

    def __init__(self):
        self.skills = {
            "SISTEMA": self._executar_sistema,
            "PROCESSOS": self._executar_processos
        }

    def listar_skills(self):
        return list(self.skills.keys())

    def executar(self, skill, comando=None):

        skill = skill.upper()

        if skill not in self.skills:
            print(f"Watari: A Skill '{skill}' não existe.")
            return

        self.skills[skill](comando)

    def _executar_sistema(self, comando=None):
        mostrar_informacoes_sistema()

    def _executar_processos(self, comando=None):
        listar_processos()