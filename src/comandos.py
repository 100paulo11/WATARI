from src.intencoes import (
    criar_intencao,
    criar_intencao_skill,
    criar_intencao_conversa,
    criar_intencao_pergunta,
    criar_intencao_desconhecida
)

from src.aplicativos import encontrar_aplicativo
from src.recursos import encontrar_site, encontrar_pasta
from src.skill_manager import SkillManager


skill_manager = SkillManager()


def normalizar_comando(comando):
    comando = comando.lower().strip()
    comando = " ".join(comando.split())

    caracteres = ["?", "!", ".", ","]

    for caractere in caracteres:
        comando = comando.replace(caractere, "")

    return comando


def identificar_intencao(comando):

    comando = normalizar_comando(comando)

    palavras_abrir = [
        "abra",
        "abre",
        "abrir",
        "pode abrir",
        "inicie",
        "iniciar"
    ]

    palavras_fechar = [
        "feche",
        "fecha",
        "fechar",
        "pode fechar",
        "encerre",
        "encerrar"
    ]

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

    if any(frase in comando for frase in palavras_sistema):
        return criar_intencao_skill("SISTEMA")

    if any(frase in comando for frase in palavras_processos):
        return criar_intencao_skill("PROCESSOS")

    if any(palavra in comando for palavra in palavras_fechar):

        aplicativo = encontrar_aplicativo(comando)

        if aplicativo:
            return criar_intencao_skill(
                "APLICATIVOS",
                "FECHAR",
                {
                    "aplicativo": aplicativo
                }
            )

        return criar_intencao_pergunta("FECHAR")

    if any(palavra in comando for palavra in palavras_abrir):

        site = encontrar_site(comando)

        if site:
            return criar_intencao(
                "ABRIR_SITE",
                site
            )

        pasta = encontrar_pasta(comando)

        if pasta:
            return criar_intencao(
                "ABRIR_PASTA",
                pasta
            )

        aplicativo = encontrar_aplicativo(comando)

        if aplicativo:
            return criar_intencao_skill(
                "APLICATIVOS",
                "ABRIR",
                {
                    "aplicativo": aplicativo
                }
            )

        return criar_intencao_pergunta("ABRIR")

    if "olá" in comando or "ola" in comando:
        return criar_intencao_conversa("SAUDACAO")

    if "seu nome" in comando:
        return criar_intencao_conversa("NOME")

    if "quem é você" in comando or "quem e voce" in comando:
        return criar_intencao_conversa("IDENTIDADE")

    return criar_intencao_desconhecida(comando)


def executar_intencao(intencao):

    acao = intencao["acao"]
    objeto = intencao["objeto"]
    parametros = intencao["parametros"]

    if acao == "SKILL":

        if parametros:
            skill_manager.executar(
                objeto,
                {
                    "acao": parametros.get("acao"),
                    "aplicativo": parametros.get("aplicativo")
                }
            )
        else:
            skill_manager.executar(objeto)

    elif acao == "ABRIR_SITE":

        from src.executor import executar_site

        executar_site(objeto)

    elif acao == "ABRIR_PASTA":

        from src.executor import executar_pasta

        executar_pasta(objeto)

    elif acao == "CONVERSAR":

        if objeto == "SAUDACAO":
            print("Watari: Olá. Como posso ajudar?")

        elif objeto == "NOME":
            print("Watari: Meu nome é Watari.")

        elif objeto == "IDENTIDADE":
            print("Watari: Eu sou o Watari, seu assistente pessoal.")

    elif acao == "PERGUNTAR":

        if objeto == "ABRIR":
            print("Watari: O que você deseja que eu abra?")

        elif objeto == "FECHAR":
            print("Watari: O que você deseja que eu feche?")

    elif acao == "DESCONHECIDO":

        print("Watari: Ainda não sei executar esse comando.")

    else:

        print("Watari: Não reconheci essa intenção.")
