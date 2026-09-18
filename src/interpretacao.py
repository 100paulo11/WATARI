from src.aplicativos import encontrar_aplicativo
from src.recursos import encontrar_site, encontrar_pasta


def normalizar_comando(comando):

    comando = comando.lower().strip()

    caracteres = ["?", "!", ".", ","]

    for caractere in caracteres:
        comando = comando.replace(
            caractere,
            ""
        )

    comando = " ".join(
        comando.split()
    )

    palavras_desnecessarias = [
        "watari",
        "por favor",
        "você pode",
        "voce pode",
        "poderia",
        "por gentileza"
    ]

    for palavra in palavras_desnecessarias:
        comando = comando.replace(
            palavra,
            " "
        )

    comando = " ".join(
        comando.split()
    )

    return comando


def identificar_acao(comando):

    comando = normalizar_comando(
        comando
    )

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

    comando = normalizar_comando(
        comando
    )

    aplicativo = encontrar_aplicativo(
        comando
    )

    if aplicativo:

        return {
            "tipo": "APLICATIVO",
            "identificador": aplicativo
        }

    site = encontrar_site(
        comando
    )

    if site:

        return {
            "tipo": "SITE",
            "identificador": site
        }

    pasta = encontrar_pasta(
        comando
    )

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


class Interpretador:

    def interpretar(self, comando):

        comando_normalizado = normalizar_comando(
            comando
        )

        return {
            "comando_original": comando,
            "comando_normalizado": comando_normalizado,
            "acao": identificar_acao(
                comando_normalizado
            ),
            "objeto": identificar_objeto(
                comando_normalizado
            ),
            "referencia": identificar_referencia(
                comando_normalizado
            )
        }