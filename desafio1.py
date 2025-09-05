menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

=> """


saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES=3

def receber_valor(nome):
    try:
        valor = float(input("Digite o valor a "+ nome + ":"))
    except ValueError:
        print ("Entrada digitada incorreta!")
        return -1;
    
    return valor


while  True:

    opcao = input(menu)
    
    if opcao == 'd':
        valor = receber_valor("Deposito")
        if (valor > 0) :
            saldo += valor
            print (f"Deposito realizado no R$ {valor:.2f}, novo saldo R$ {saldo:.2f}")
            extrato += f"Deposito: R$ {valor:.2f}\n"
        else:
            print("Deposito Inválido!")

    elif opcao == "s":
        valor = receber_valor("Sacar")

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite diário.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            print (f"Realizado um saque no valor de {valor}")      
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques +=1
        else:
            print("Operação falhou! O valor informado é inválido.")

        
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break
    
    else:
        print ("Opção inválida, por favor tenten novamente a operação desejada")

    

