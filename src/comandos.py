from src.executor import (
    executar_abrir,
    executar_fechar,
    executar_site,
    executar_pasta
)

from src.intencoes import criar_intencao
from src.aplicativos import encontrar_aplicativo
from src.recursos import encontrar_site, encontrar_pasta
from src.skill_manager import SkillManager


skill_manager = SkillManager()


def normalizar_comando(comando):
    comando = comando.lower().strip()
    comando = " ".join(comando.split())
    comando = comando.replace("?", "")
    comando = comando.replace("!", "")
    comando = comando.replace(".", "")
    comando = comando.replace(",", "")

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
        return criar_intencao("SKILL", "SISTEMA")

    if any(frase in comando for frase in palavras_processos):
        return criar_intencao("SKILL", "PROCESSOS")

    if any(palavra in comando for palavra in palavras_fechar):
        aplicativo = encontrar_aplicativo(comando)

        if aplicativo:
            return criar_intencao("FECHAR", aplicativo)

        return criar_intencao("PERGUNTAR", "FECHAR")

    if any(palavra in comando for palavra in palavras_abrir):
        site = encontrar_site(comando)

        if site:
            return criar_intencao("ABRIR_SITE", site)

        pasta = encontrar_pasta(comando)

        if pasta:
            return criar_intencao("ABRIR_PASTA", pasta)

        aplicativo = encontrar_aplicativo(comando)

        if aplicativo:
            return criar_intencao("ABRIR", aplicativo)

        return criar_intencao("PERGUNTAR", "ABRIR")

    if "olá" in comando or "ola" in comando:
        return criar_intencao("CONVERSAR", "SAUDACAO")

    if "seu nome" in comando:
        return criar_intencao("CONVERSAR", "NOME")

    if "quem é você" in comando or "quem e voce" in comando:
        return criar_intencao("CONVERSAR", "IDENTIDADE")

    return criar_intencao("DESCONHECIDO", "NENHUM")


def executar_intencao(intencao):
    acao = intencao["acao"]
    objeto = intencao["objeto"]

    if acao == "SKILL":
        skill_manager.executar(objeto)

    elif acao == "ABRIR":
        executar_abrir(objeto)

    elif acao == "FECHAR":
        executar_fechar(objeto)

    elif acao == "ABRIR_SITE":
        executar_site(objeto)

    elif acao == "ABRIR_PASTA":
        executar_pasta(objeto)

    elif acao == "CONVERSAR" and objeto == "SAUDACAO":
        print("Watari: Olá. Como posso ajudar?")

    elif acao == "CONVERSAR" and objeto == "NOME":
        print("Watari: Meu nome é Watari.")

    elif acao == "CONVERSAR" and objeto == "IDENTIDADE":
        print("Watari: Eu sou o Watari, seu assistente pessoal.")

    elif acao == "PERGUNTAR" and objeto == "ABRIR":
        print("Watari: O que você deseja que eu abra?")

    elif acao == "PERGUNTAR" and objeto == "FECHAR":
        print("Watari: O que você deseja que eu feche?")

    else:
        print("Watari: Ainda não sei executar esse comando.")