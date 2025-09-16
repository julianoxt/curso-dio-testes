import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


#o caracter / demilita que são apenas positional only
def depositar (saldo, valor, extrato,/):
    if (valor > 0) :
        saldo += valor
        print (f"Deposito realizado no R$ {valor:.2f}, novo saldo R$ {saldo:.2f}")
        extrato += f"Deposito: R$ {valor:.2f}\n"
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato


# o caracter * delimita que os argumentos são apenas keyword only
def sacar(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

#argumentos posicionais saldo / argumentos nomeados extrato
def imprimir_extrato(saldo, /, *,extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

# o endereço deve ser informado  no formato: logratouro , num - bairro- cidade/estado
#deve ser armazenado somente os numeros do cpf , não pode cadastra 2 usuários com o mesmo cpf
def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

#O numero da conta é composta por : agencia, numer_conta e usuario
#um usuário pode ter uma conta mais uma conta so pertece a um usuario/
def cadastrar_conta_corrente(agencia,numero_conta,usuarios):
    cpf = input("Digite o CPF do usuário: ")
    usuario = filtrar_usuario(cpf=cpf,usuarios=usuarios)
    
    if usuario: 
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia":agencia, "numero_conta'" : numero_conta,"usuario":usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
        Agência:\t{conta['agencia']}
        C/C:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 0)
        print(textwrap.dedent(linha))

def receber_valor(nome):
    try:
        valor = float(input("Digite o valor a "+ nome + ":"))
    except ValueError:
        print ("Entrada digitada incorreta!")
        return -1;
    
    return valor

def main():
    usuarios = []
    contas_correntes =[]
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES=3
    AGENCIA="0001"




    while  True:

        opcao = menu()
        
        if opcao == 'd':
            valor = receber_valor("depositar")
            saldo,extrato = depositar(saldo,valor,extrato)
        elif opcao == "s":
            valor = receber_valor("sacar")
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            imprimir_extrato(saldo,extrato=extrato,)
        elif opcao == "nc":
            numero_conta=len(contas_correntes) + 1
            conta = cadastrar_conta_corrente(agencia=AGENCIA,numero_conta=numero_conta,usuarios=usuarios)
            if conta:
                contas_correntes.append(conta)
                print("\n@@@ Conta cadastrada com sucesso! @@@")
            
        elif opcao == "lc":
            listar_contas(contas_correntes)
        elif opcao == "nu":
            cadastrar_usuario(usuarios)
        elif opcao == "q":
            break
        
        else:
            print ("Opção inválida, por favor tenten novamente a operação desejada")

    
main()
