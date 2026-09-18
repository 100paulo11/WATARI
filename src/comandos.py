from src.intencoes import (
    criar_intencao,
    criar_intencao_skill,
    criar_intencao_conversa,
    criar_intencao_pergunta,
    criar_intencao_referencia,
    criar_intencao_desconhecida
)

from src.aplicativos import encontrar_aplicativo
from src.recursos import encontrar_site, encontrar_pasta
from src.skill_manager import SkillManager


skill_manager = SkillManager()


def normalizar_comando(comando):
    comando = comando.lower().strip()

    caracteres = ["?", "!", ".", ","]

    for caractere in caracteres:
        comando = comando.replace(caractere, "")

    comando = " ".join(comando.split())

    palavras_desnecessarias = [
        "watari",
        "por favor",
        "você pode",
        "voce pode",
        "poderia",
        "por gentileza"
    ]

    for palavra in palavras_desnecessarias:
        comando = comando.replace(palavra, " ")

    comando = " ".join(comando.split())

    return comando


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


def identificar_acao(comando):

    comando = normalizar_comando(comando)

    palavras_abrir = [
        "abra",
        "abre",
        "abrir",
        "inicie",
        "iniciar",
        "comece",
        "começar",
        "quero abrir",
        "quero iniciar",
        "pode abrir",
        "pode iniciar",
        "consegue abrir",
        "consegue iniciar",
        "gostaria de abrir",
        "gostaria de iniciar"
    ]

    palavras_fechar = [
        "feche",
        "fecha",
        "fechar",
        "encerre",
        "encerrar",
        "termine",
        "terminar",
        "quero fechar",
        "quero encerrar",
        "pode fechar",
        "pode encerrar",
        "consegue fechar",
        "consegue encerrar",
        "gostaria de fechar"
    ]

    for palavra in palavras_abrir:
        if palavra in comando:
            return "ABRIR"

    for palavra in palavras_fechar:
        if palavra in comando:
            return "FECHAR"

    return None


def identificar_objeto(comando):

    comando = normalizar_comando(comando)

    aplicativo = encontrar_aplicativo(comando)

    if aplicativo:
        return {
            "tipo": "APLICATIVO",
            "identificador": aplicativo
        }

    site = encontrar_site(comando)

    if site:
        return {
            "tipo": "SITE",
            "identificador": site
        }

    pasta = encontrar_pasta(comando)

    if pasta:
        return {
            "tipo": "PASTA",
            "identificador": pasta
        }

    return None


def identificar_referencia(comando):

    referencias = [
        "ele",
        "ela",
        "isso",
        "esse",
        "essa",
        "esse aplicativo",
        "essa aplicação",
        "esse programa",
        "o último",
        "o ultimo",
        "a última",
        "a ultima"
    ]

    for referencia in referencias:
        if referencia in comando:
            return referencia

    return None


def identificar_intencao(comando):

    comando = normalizar_comando(comando)

    acao = identificar_acao(comando)
    objeto = identificar_objeto(comando)

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

    referencia = identificar_referencia(comando)

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
        acao_referencia = parametros.get("acao")

        entidade = contexto.obter_ultima_entidade()

        if entidade is None:
            print(
                "Watari: Não sei a que você está "
                "se referindo."
            )
            return

        tipo = entidade.get("tipo")
        identificador = entidade.get("identificador")

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

        acao_skill = parametros.get("acao")

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