def criar_intencao(acao, objeto=None, parametros=None):
    return {
        "acao": acao,
        "objeto": objeto,
        "parametros": parametros or {}
    }


def criar_intencao_skill(skill, acao=None, parametros=None):
    return criar_intencao(
        "SKILL",
        skill,
        {
            "acao": acao,
            **(parametros or {})
        }
    )


def criar_intencao_conversa(tipo, parametros=None):
    return criar_intencao(
        "CONVERSAR",
        tipo,
        parametros
    )


def criar_intencao_pergunta(tipo, parametros=None):
    return criar_intencao(
        "PERGUNTAR",
        tipo,
        parametros
    )


def criar_intencao_referencia(referencia, acao=None):
    return criar_intencao(
        "REFERENCIA",
        referencia,
        {
            "acao": acao
        }
    )


def criar_intencao_desconhecida(comando=None):
    return criar_intencao(
        "DESCONHECIDO",
        comando
    )