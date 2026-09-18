import subprocess


APLICATIVOS = {
    "BLOCO_NOTAS": {
        "nome": "Bloco de Notas",
        "aliases": [
            "bloco de notas",
            "bloco de nota",
            "notepad",
            "editor de texto"
        ],
        "comando_abrir": ["notepad.exe"],
        "processo": "notepad.exe"
    },

    "CALCULADORA": {
        "nome": "Calculadora",
        "aliases": [
            "calculadora",
            "calc"
        ],
        "comando_abrir": ["calc.exe"],
        "processo": "CalculatorApp.exe"
    },

    "CHROME": {
        "nome": "Google Chrome",
        "aliases": [
            "chrome",
            "google chrome",
            "navegador",
            "browser",
            "google"
        ],
        "comando_abrir": ["cmd", "/c", "start", "chrome"],
        "processo": "chrome.exe"
    }
}


def encontrar_aplicativo(nome_informado):
    nome_informado = nome_informado.lower().strip()

    for identificador, dados in APLICATIVOS.items():

        for alias in dados["aliases"]:

            if alias in nome_informado:
                return identificador

    return None


def abrir_aplicativo(aplicativo):
    dados = APLICATIVOS.get(aplicativo)

    if dados is None:
        print("Watari: Não conheço esse aplicativo.")
        return

    print(f"Watari: Abrindo o {dados['nome']}.")
    subprocess.Popen(dados["comando_abrir"])


def fechar_aplicativo(aplicativo):
    dados = APLICATIVOS.get(aplicativo)

    if dados is None:
        print("Watari: Não conheço esse aplicativo.")
        return

    print(f"Watari: Fechando o {dados['nome']}.")
    subprocess.run(
        ["taskkill", "/IM", dados["processo"], "/F"],
        capture_output=True
    )