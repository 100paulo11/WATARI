from src.comandos import (
    identificar_intencao,
    executar_intencao,
    dividir_comandos
)

from src.contexto import Contexto
from src.voz import ReconhecedorDeVoz


print("================================")
print("        WATARI INICIADO")
print("================================")
print()
print("Modo de entrada: VOZ")
print()
print("Diga 'encerrar' ou 'sair' para sair.")
print()


contexto = Contexto()

reconhecedor = ReconhecedorDeVoz(
    dispositivo=1
)


def deve_encerrar(comando):

    comando = comando.lower().strip()

    comando = comando.replace(
        "?",
        ""
    )

    comando = " ".join(
        comando.split()
    )

    comandos_encerramento = [
        "encerrar",
        "encerra",
        "encerre",
        "sair",
        "saia",
        "finalizar",
        "finaliza",
        "finalize",
        "parar",
        "pare",
        "fechar watari",
        "feche watari",
        "fechar o watari",
        "feche o watari",
        "encerrar watari",
        "encerra watari",
        "encerre watari",
        "encerrar o watari",
        "encerra o watari",
        "encerre o watari",
        "encerrar atari",
        "encerra atari",
        "encerre atari",
        "encerrar o atari",
        "encerra o atari",
        "encerre o atari",
        "sair watari",
        "sair atari",
        "finalizar watari",
        "finalizar atari"
    ]

    return comando in comandos_encerramento


while True:

    comando = reconhecedor.reconhecer(
        duracao=5
    )

    if comando is None:
        continue

    print(
        f"Você: {comando}"
    )

    if deve_encerrar(comando):

        print(
            "Watari: Encerrando."
        )

        break

    if not comando.strip():
        continue

    comandos = dividir_comandos(
        comando
    )

    for comando_individual in comandos:

        if deve_encerrar(comando_individual):

            print(
                "Watari: Encerrando."
            )

            raise SystemExit

        contexto_pendente = contexto.obter(
            "acao_pendente"
        )

        if contexto_pendente is not None:

            if contexto_pendente == "ABRIR":

                comando_completo = (
                    "abrir "
                    + comando_individual
                )

            elif contexto_pendente == "FECHAR":

                comando_completo = (
                    "fechar "
                    + comando_individual
                )

            else:

                comando_completo = (
                    comando_individual
                )

            intencao = identificar_intencao(
                comando_completo
            )

            contexto.remover(
                "acao_pendente"
            )

        else:

            intencao = identificar_intencao(
                comando_individual
            )

        contexto.adicionar_historico(
            comando_individual,
            intencao
        )

        if intencao["acao"] == "PERGUNTAR":

            contexto.definir(
                "acao_pendente",
                intencao["objeto"]
            )

        if (
            intencao["acao"] == "EXECUTAR_SKILL"
            and intencao["objeto"] == "APLICATIVOS"
        ):

            aplicativo = (
                intencao["parametros"].get(
                    "aplicativo"
                )
            )

            acao = (
                intencao["parametros"].get(
                    "acao"
                )
            )

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
                "ultimo_pasta",
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
            comando_individual
        )

        executar_intencao(
            intencao,
            contexto
        )