import subprocess


def listar_processos():
    resultado = subprocess.run(
        ["tasklist"],
        capture_output=True,
        text=True,
        encoding="cp850",
        errors="replace"
    )

    print("Watari: Processos em execução:")
    print()
    print(resultado.stdout)


def encerrar_processo(nome):
    print(f"Watari: Tentando encerrar {nome}.")

    resultado = subprocess.run(
        ["taskkill", "/IM", nome, "/F"],
        capture_output=True,
        text=True,
        encoding="cp850",
        errors="replace"
    )

    if resultado.returncode == 0:
        print("Watari: Processo encerrado.")
    else:
        print("Watari: Não consegui encerrar esse processo.")
        print(resultado.stderr)
