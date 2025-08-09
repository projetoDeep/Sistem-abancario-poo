from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict
import uuid

class Cliente:
    def __init__(self, nome: str, cpf: str, endereco: str):
        self.nome = nome
        self._cpf = cpf
        self.endereco = endereco
        self.contas: List[Conta] = []

    @property
    def cpf(self) -> str:
        return self._cpf

    def adicionar_conta(self, conta: 'Conta') -> None:
        self.contas.append(conta)

    def listar_contas(self) -> List['Conta']:
        return self.contas

class Conta(ABC):
    def __init__(self, cliente: Cliente, saldo_inicial: float = 0):
        self._numero = str(uuid.uuid4())[:8]
        self._saldo = saldo_inicial
        self._cliente = cliente
        self._historico = []
        cliente.adicionar_conta(self)

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            self._registrar_transacao("Depósito", valor)
            return True
        return False

    def sacar(self, valor: float) -> bool:
        if 0 < valor <= self._saldo:
            self._saldo -= valor
            self._registrar_transacao("Saque", -valor)
            return True
        return False

    def _registrar_transacao(self, tipo: str, valor: float) -> None:
        transacao = {
            "tipo": tipo,
            "valor": valor,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "saldo_resultante": self._saldo
        }
        self._historico.append(transacao)

    def extrato(self) -> List[Dict]:
        return self._historico

    @abstractmethod
    def tipo_conta(self) -> str:
        pass

class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, limite: float = 1000, saldo_inicial: float = 0):
        super().__init__(cliente, saldo_inicial)
        self._limite = limite

    def sacar(self, valor: float) -> bool:
        if 0 < valor <= (self._saldo + self._limite):
            self._saldo -= valor
            self._registrar_transacao("Saque", -valor)
            return True
        return False

    def tipo_conta(self) -> str:
        return "Conta Corrente"

class ContaPoupanca(Conta):
    def __init__(self, cliente: Cliente, taxa_juros: float = 0.005, saldo_inicial: float = 0):
        super().__init__(cliente, saldo_inicial)
        self._taxa_juros = taxa_juros

    def aplicar_juros(self) -> None:
        juros = self._saldo * self._taxa_juros
        self._saldo += juros
        self._registrar_transacao("Juros", juros)

    def tipo_conta(self) -> str:
        return "Conta Poupança"

class Banco:
    def __init__(self, nome: str):
        self.nome = nome
        self._clientes: Dict[str, Cliente] = {}
        self._contas: Dict[str, Conta] = {}

    def cadastrar_cliente(self, nome: str, cpf: str, endereco: str) -> Cliente:
        if cpf not in self._clientes:
            cliente = Cliente(nome, cpf, endereco)
            self._clientes[cpf] = cliente
            return cliente
        raise ValueError("Cliente já cadastrado")

    def criar_conta_corrente(self, cpf: str, limite: float = 1000, saldo_inicial: float = 0) -> ContaCorrente:
        cliente = self._clientes.get(cpf)
        if cliente:
            conta = ContaCorrente(cliente, limite, saldo_inicial)
            self._contas[conta.numero] = conta
            return conta
        raise ValueError("Cliente não encontrado")

    def criar_conta_poupanca(self, cpf: str, taxa_juros: float = 0.005, saldo_inicial: float = 0) -> ContaPoupanca:
        cliente = self._clientes.get(cpf)
        if cliente:
            conta = ContaPoupanca(cliente, taxa_juros, saldo_inicial)
            self._contas[conta.numero] = conta
            return conta
        raise ValueError("Cliente não encontrado")

    def buscar_conta(self, numero_conta: str) -> Conta:
        conta = self._contas.get(numero_conta)
        if conta:
            return conta
        raise ValueError("Conta não encontrada")

    def buscar_cliente(self, cpf: str) -> Cliente:
        cliente = self._clientes.get(cpf)
        if cliente:
            return cliente
        raise ValueError("Cliente não encontrado")

    def listar_contas_cliente(self, cpf: str) -> List[Conta]:
        cliente = self.buscar_cliente(cpf)
        return cliente.listar_contas()

# Exemplo de uso do sistema
def main():
    # Criando banco
    banco = Banco("Banco Python")

    try:
        # Cadastrando cliente
        cliente = banco.cadastrar_cliente("João Silva", "123.456.789-00", "Rua Python, 123")
        
        # Criando contas
        conta_corrente = banco.criar_conta_corrente("123.456.789-00", limite=2000, saldo_inicial=1000)
        conta_poupanca = banco.criar_conta_poupanca("123.456.789-00", taxa_juros=0.01, saldo_inicial=500)

        # Realizando operações
        print(f"Saldo inicial CC: R${conta_corrente.saldo:.2f}")
        conta_corrente.depositar(500)
        print(f"Saldo após depósito: R${conta_corrente.saldo:.2f}")
        conta_corrente.sacar(300)
        print(f"Saldo após saque: R${conta_corrente.saldo:.2f}")

        print("\nConta Poupança:")
        print(f"Saldo inicial: R${conta_poupanca.saldo:.2f}")
        conta_poupanca.aplicar_juros()
        print(f"Saldo após juros: R${conta_poupanca.saldo:.2f}")

        # Imprimindo extrato
        print("\nExtrato Conta Corrente:")
        for transacao in conta_corrente.extrato():
            print(f"Tipo: {transacao['tipo']}, Valor: R${transacao['valor']:.2f}, "
                  f"Data: {transacao['data']}, Saldo: R${transacao['saldo_resultante']:.2f}")

    except ValueError as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
