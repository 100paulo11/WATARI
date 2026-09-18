import os
import webbrowser


SITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com"
}


PASTAS = {
    "downloads": os.path.expanduser("~/Downloads"),
    "documentos": os.path.expanduser("~/Documents"),
    "desktop": os.path.expanduser("~/Desktop")
}


def encontrar_site(nome_informado):
    nome_informado = nome_informado.lower().strip()

    for nome, url in SITES.items():
        if nome in nome_informado:
            return url

    return None


def encontrar_pasta(nome_informado):
    nome_informado = nome_informado.lower().strip()

    for nome, caminho in PASTAS.items():
        if nome in nome_informado:
            return caminho

    return None


def abrir_site(url):
    print(f"Watari: Abrindo {url}.")
    webbrowser.open(url)


def abrir_pasta(caminho):
    print(f"Watari: Abrindo a pasta.")
    os.startfile(caminho)
