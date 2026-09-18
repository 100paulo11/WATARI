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

        if aplicativo is not None:

            contexto.definir(
                "ultimo_aplicativo",
                aplicativo
            )

    executar_intencao(
        intencao,
        contexto
    )