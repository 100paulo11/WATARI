from src.comandos import identificar_intencao, executar_intencao
from src.contexto import Contexto


print("================================")
print("        WATARI INICIADO")
print("================================")
print()
print("Digite 'sair' para encerrar.")
print()


contexto = Contexto()


while True:

    comando = input("Você: ")

    if comando.lower().strip() == "sair":
        print("Watari: Encerrando.")
        break

    if not comando.strip():
        continue

    contexto_pendente = contexto.obter("acao_pendente")

    if contexto_pendente is not None:

        if contexto_pendente == "ABRIR":
            comando_completo = "abrir " + comando

        elif contexto_pendente == "FECHAR":
            comando_completo = "fechar " + comando

        else:
            comando_completo = comando

        intencao = identificar_intencao(comando_completo)

        contexto.remover("acao_pendente")

    else:

        intencao = identificar_intencao(comando)

    contexto.adicionar_historico(
        comando,
        intencao
    )

    if intencao["acao"] == "PERGUNTAR":

        contexto.definir(
            "acao_pendente",
            intencao["objeto"]
        )

    if (
        intencao["acao"] == "SKILL"
        and intencao["objeto"] == "APLICATIVOS"
    ):

        aplicativo = intencao["parametros"].get("aplicativo")
        acao = intencao["parametros"].get("acao")

        if aplicativo is not None:

            contexto.definir(
                "ultimo_aplicativo",
                aplicativo
            )

            contexto.definir(
                "ultima_acao",
                acao
            )

            contexto.definir_ultima_entidade(
                "APLICATIVO",
                aplicativo
            )

    elif intencao["acao"] == "ABRIR_SITE":

        contexto.definir(
            "ultimo_site",
            intencao["objeto"]
        )

        contexto.definir(
            "ultima_acao",
            "ABRIR_SITE"
        )

        contexto.definir_ultima_entidade(
            "SITE",
            intencao["objeto"]
        )

    elif intencao["acao"] == "ABRIR_PASTA":

        contexto.definir(
            "ultima_pasta",
            intencao["objeto"]
        )

        contexto.definir(
            "ultima_acao",
            "ABRIR_PASTA"
        )

        contexto.definir_ultima_entidade(
            "PASTA",
            intencao["objeto"]
        )

    contexto.definir(
        "ultimo_comando",
        comando
    )

    executar_intencao(
        intencao,
        contexto
    )