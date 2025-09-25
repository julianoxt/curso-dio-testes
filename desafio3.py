from abc import ABC, abstractmethod
import datetime
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
        #faz um relacionamento com o historico
        self._historico = Historico()

    #insanciar a mesma clase da forma correta
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente,numero) 
    #acessar atributos privados através do método
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def hitorico(self):
        return self._historico
    
    def saldo(self, valor):
        return valor

    def sacar(self, valor):
        saldo = self.saldo

        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self,valor):
        if (valor > 0) :
            self._saldo += valor
            print("\n=== Deposito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
    
    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

class ContaCorrente(Conta):
    def __init__(self, limite=500, limite_saques=3,**kw):
        super().__init__(**kw)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        #define o numero de saques baseado no historico de transações
        numero_saques = len(
            [Trasacao for transacao in self.hitorico.trasacoes if transacao[tipo] == "Saque"
             ]
        )
        
        excedeu_limite = valor > self._limite
        excedeu_saques = valor >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else: 
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
                Agência;\t{self.agencia}
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

        if(sucesso_transacao):
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
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento,**kw):
        super().__init__(**kw)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

class ContaCorrente:
    pass

