from src.comandos import identificar_intencao, executar_intencao


print("================================")
print("        WATARI INICIADO")
print("================================")
print()
print("Digite 'sair' para encerrar.")
print()


contexto = None


while True:
    comando = input("Você: ")

    if comando.lower().strip() == "sair":
        print("Watari: Encerrando.")
        break

    if not comando.strip():
        continue

    if contexto is not None:
        if contexto == "ABRIR":
            comando_completo = "abrir " + comando

        elif contexto == "FECHAR":
            comando_completo = "fechar " + comando

        else:
            comando_completo = comando

        intencao = identificar_intencao(comando_completo)
        contexto = None

    else:
        intencao = identificar_intencao(comando)

    if intencao["acao"] == "PERGUNTAR":
        contexto = intencao["objeto"]

    executar_intencao(intencao)