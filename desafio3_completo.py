from abc import ABC, abstractmethod, abstractclassmethod
from datetime import datetime
import textwrap




class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Conta:
    
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True



class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    

class Trasacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self,conta):
        pass

class Deposito(Trasacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Trasacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if(sucesso_transacao):
            conta.historico.adicionar_transacao(self)

class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento,endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


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

def filtra_clientes(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf==cpf]
    #retorna clientes filtrados caso o clientes filtrados não esteja vazio
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
            print("\n@@@ Cliente não possui conta! @@@")
    # FIXME: não permite o cliente escolher a conta 
    return cliente.contas[0]

#criar função que retone o cliente como meloria de codigo
##criar função que receba uma instancia de transação e efetue o metodo, de forma qu simplifique o deposita
#e a função sacar

def depositar (clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtra_clientes(cpf,clientes)

    if not cliente:
        print ("\@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do deposito:"))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)


def sacar (clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtra_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtra_clientes(cpf,clientes)

    if not cliente:
        print ("\@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n ============= EXTRATO ==============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n {transacao['tipo']}:\n \t R${transacao['valor']:.2f}"

        print(extrato)
        print(f"\nSaldo:\n\t$R$ {conta.saldo:.2f}")
        print("=====================================")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtra_clientes(cpf,clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrato, fluxo de criação" \
        "de conta finalizado!@@@")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n ====== Conta criada com sucesso! ======")

def lista_contas(contas):
    for conta in contas:
       print("="*100)
       print(textwrap.dedent(str(conta)))

def criar_clientes(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtra_clientes(cpf,clientes)

    if  cliente:
        print("\n@@@ Cliente já cadastrado com o CPF@@@")
        return
    
    nome = input("Informe o nome completo")
    data_nascimento = input("Informe data de nascimento (dd-mm-aaaa)")
    endereco = input("Informe o endereço (logradouro, nro, bairro, cidade/estado)")

    cliente= PessoaFisica(cpf=cpf,nome=nome,data_nascimento=data_nascimento,endereco=endereco)

    clientes.append(cliente)

    print("\n === Cliente criado com sucesso ===")


def main():
    clientes = []
    contas = []

    while  True:

        opcao = menu()

        if opcao == 'd':
            depositar(clientes)
        elif opcao == "s":
             sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nc":
            numero_conta = len(contas)+1
            criar_conta(numero_conta,clientes,contas)
        elif opcao == "lc":
            lista_contas(contas)
        elif opcao == "nu":
            criar_clientes(clientes)
        elif opcao == "q":
            break

        else:
            print ("Opção inválida, por favor tenten novamente a operação desejada")

main()