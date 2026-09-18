from src.intencoes import (
    criar_intencao,
    criar_intencao_skill,
    criar_intencao_conversa,
    criar_intencao_pergunta,
    criar_intencao_referencia,
    criar_intencao_desconhecida
)

from src.interpretacao import (
    normalizar_comando,
    identificar_acao,
    identificar_objeto,
    identificar_referencia
)

from src.skill_manager import SkillManager


skill_manager = SkillManager()


def dividir_comandos(comando):

    separadores = [
        " e depois ",
        " depois ",
        " e então ",
        " e entao ",
        " então ",
        " entao "
    ]

    partes = [comando]

    for separador in separadores:

        novas_partes = []

        for parte in partes:

            novas_partes.extend(
                parte.split(separador)
            )

        partes = novas_partes

    return [
        parte.strip()
        for parte in partes
        if parte.strip()
    ]


def identificar_intencao(comando):

    comando = normalizar_comando(
        comando
    )

    acao = identificar_acao(
        comando
    )

    objeto = identificar_objeto(
        comando
    )

    referencia = identificar_referencia(
        comando
    )

    palavras_sistema = [
        "informações do sistema",
        "informacoes do sistema",
        "informações sobre o sistema",
        "informacoes sobre o sistema",
        "dados do sistema",
        "informações do computador",
        "informacoes do computador",
        "dados do computador",
        "meu computador",
        "configuração do computador",
        "configuracao do computador"
    ]

    palavras_processos = [
        "listar processos",
        "liste processos",
        "liste os processos",
        "listar os processos",
        "mostrar processos",
        "mostrar os processos",
        "mostre processos",
        "mostre os processos",
        "processos em execução",
        "processos em execucao",
        "processos rodando",
        "processos abertos"
    ]

    if referencia is not None:

        if acao == "FECHAR":

            return criar_intencao_referencia(
                referencia,
                "FECHAR"
            )

        if acao == "ABRIR":

            return criar_intencao_referencia(
                referencia,
                "ABRIR"
            )

    if any(
        frase in comando
        for frase in palavras_sistema
    ):

        return criar_intencao_skill(
            "SISTEMA"
        )

    if any(
        frase in comando
        for frase in palavras_processos
    ):

        return criar_intencao_skill(
            "PROCESSOS"
        )

    if acao == "FECHAR":

        if objeto and objeto["tipo"] == "APLICATIVO":

            return criar_intencao_skill(
                "APLICATIVOS",
                "FECHAR",
                {
                    "aplicativo": objeto["identificador"]
                }
            )

        return criar_intencao_pergunta(
            "FECHAR"
        )

    if acao == "ABRIR":

        if objeto and objeto["tipo"] == "SITE":

            return criar_intencao(
                "ABRIR_SITE",
                objeto["identificador"]
            )

        if objeto and objeto["tipo"] == "PASTA":

            return criar_intencao(
                "ABRIR_PASTA",
                objeto["identificador"]
            )

        if objeto and objeto["tipo"] == "APLICATIVO":

            return criar_intencao_skill(
                "APLICATIVOS",
                "ABRIR",
                {
                    "aplicativo": objeto["identificador"]
                }
            )

        return criar_intencao_pergunta(
            "ABRIR"
        )

    if "olá" in comando or "ola" in comando:

        return criar_intencao_conversa(
            "SAUDACAO"
        )

    if "seu nome" in comando:

        return criar_intencao_conversa(
            "NOME"
        )

    if (
        "quem é você" in comando
        or "quem e voce" in comando
    ):

        return criar_intencao_conversa(
            "IDENTIDADE"
        )

    return criar_intencao_desconhecida(
        comando
    )


def executar_intencao(intencao, contexto=None):

    acao = intencao["acao"]
    objeto = intencao["objeto"]
    parametros = intencao["parametros"]

    if acao == "REFERENCIA":

        if contexto is None:

            print(
                "Watari: Não tenho contexto suficiente "
                "para isso."
            )

            return

        referencia = objeto

        acao_referencia = parametros.get(
            "acao"
        )

        entidade = contexto.obter_ultima_entidade()

        if entidade is None:

            print(
                "Watari: Não sei a que você está "
                "se referindo."
            )

            return

        tipo = entidade.get("tipo")

        identificador = entidade.get(
            "identificador"
        )

        if tipo == "APLICATIVO":

            nova_intencao = criar_intencao_skill(
                "APLICATIVOS",
                acao_referencia,
                {
                    "aplicativo": identificador
                }
            )

            executar_intencao(
                nova_intencao,
                contexto
            )

        elif tipo == "SITE":

            if acao_referencia == "ABRIR":

                nova_intencao = criar_intencao(
                    "ABRIR_SITE",
                    identificador
                )

                executar_intencao(
                    nova_intencao,
                    contexto
                )

            elif acao_referencia == "FECHAR":

                nova_intencao = criar_intencao_skill(
                    "NAVEGADOR",
                    "FECHAR"
                )

                executar_intencao(
                    nova_intencao,
                    contexto
                )

            else:

                print(
                    "Watari: Ainda não sei executar "
                    "essa ação para um site."
                )

        elif tipo == "PASTA":

            if acao_referencia == "ABRIR":

                nova_intencao = criar_intencao(
                    "ABRIR_PASTA",
                    identificador
                )

                executar_intencao(
                    nova_intencao,
                    contexto
                )

            else:

                print(
                    "Watari: Ainda não sei fechar "
                    "esse tipo de entidade."
                )

        return

    if acao == "EXECUTAR_SKILL":

        acao_skill = parametros.get(
            "acao"
        )

        dados_skill = parametros.copy()

        dados_skill["acao"] = acao_skill

        skill_manager.executar(
            objeto,
            dados_skill
        )

    elif acao == "ABRIR_SITE":

        from src.executor import executar_site

        executar_site(
            objeto
        )

    elif acao == "ABRIR_PASTA":

        from src.executor import executar_pasta

        executar_pasta(
            objeto
        )

    elif acao == "CONVERSAR":

        if objeto == "SAUDACAO":

            print(
                "Watari: Olá. Como posso ajudar?"
            )

        elif objeto == "NOME":

            print(
                "Watari: Meu nome é Watari."
            )

        elif objeto == "IDENTIDADE":

            print(
                "Watari: Eu sou o Watari, "
                "seu assistente pessoal."
            )

    elif acao == "PERGUNTAR":

        if objeto == "ABRIR":

            print(
                "Watari: O que você deseja "
                "que eu abra?"
            )

        elif objeto == "FECHAR":

            print(
                "Watari: O que você deseja "
                "que eu feche?"
            )

    elif acao == "DESCONHECIDO":

        print(
            "Watari: Ainda não sei executar "
            "esse comando."
        )

    else:

        print(
            "Watari: Não reconheci essa intenção."
        )