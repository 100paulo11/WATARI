import platform
import shutil


def obter_informacoes_sistema():
    sistema = platform.system()
    versao = platform.version()
    arquitetura = platform.machine()
    processador = platform.processor()

    armazenamento = shutil.disk_usage("/")

    return {
        "sistema": sistema,
        "versao": versao,
        "arquitetura": arquitetura,
        "processador": processador,
        "armazenamento_total": armazenamento.total,
        "armazenamento_usado": armazenamento.used,
        "armazenamento_livre": armazenamento.free
    }


def mostrar_informacoes_sistema():
    informacoes = obter_informacoes_sistema()

    print("Watari: Estas são as informações do sistema:")
    print()

    print(f"Sistema: {informacoes['sistema']}")
    print(f"Versão: {informacoes['versao']}")
    print(f"Arquitetura: {informacoes['arquitetura']}")
    print(f"Processador: {informacoes['processador']}")

    total_gb = informacoes["armazenamento_total"] / (1024 ** 3)
    usado_gb = informacoes["armazenamento_usado"] / (1024 ** 3)
    livre_gb = informacoes["armazenamento_livre"] / (1024 ** 3)

    print(f"Armazenamento total: {total_gb:.2f} GB")
    print(f"Armazenamento usado: {usado_gb:.2f} GB")
    print(f"Armazenamento livre: {livre_gb:.2f} GB")