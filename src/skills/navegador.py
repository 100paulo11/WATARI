import subprocess


def fechar_navegador():
    print("Watari: Fechando o navegador.")

    resultado = subprocess.run(
        ["taskkill", "/IM", "chrome.exe", "/F"],
        capture_output=True,
        text=True,
        encoding="cp850",
        errors="replace"
    )

    if resultado.returncode == 0:
        print("Watari: Navegador fechado.")
    else:
        print("Watari: O navegador não estava aberto.")