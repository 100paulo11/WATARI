from src.aplicativos import abrir_aplicativo, fechar_aplicativo
from src.recursos import abrir_site, abrir_pasta


def executar_abrir(aplicativo):
    abrir_aplicativo(aplicativo)


def executar_fechar(aplicativo):
    fechar_aplicativo(aplicativo)


def executar_site(site):
    abrir_site(site)


def executar_pasta(pasta):
    abrir_pasta(pasta)