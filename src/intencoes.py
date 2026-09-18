def criar_intencao(acao, objeto=None, parametros=None):
    return {
        "acao": acao,
        "objeto": objeto,
        "parametros": parametros or {}
    }


def criar_intencao_acao(acao, objeto=None, parametros=None):
    return criar_intencao(
        acao,
        objeto,
        parametros
    )


def criar_intencao_skill(skill, acao=None, parametros=None):
    dados = parametros.copy() if parametros else {}

    if acao is not None:
        dados["acao"] = acao

    return criar_intencao(
        "EXECUTAR_SKILL",
        skill,
        dados
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