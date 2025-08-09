from flask import Flask, render_template, request, jsonify
from datetime import datetime
import uuid

# Importando as classes do sistema bancário
from banco import Banco, Cliente, ContaCorrente, ContaPoupanca

app = Flask(__name__)

# Criando uma instância do banco
banco = Banco("Banco Python")

@app.route('/')
def index():
    """Rota principal que renderiza o template HTML"""
    return render_template('index.html')

@app.route('/api/cliente', methods=['POST'])
def cadastrar_cliente():
    """API para cadastrar um novo cliente"""
    try:
        data = request.json
        cliente = banco.cadastrar_cliente(
            nome=data['nome'],
            cpf=data['cpf'],
            endereco=data['endereco']
        )
        return jsonify({
            'message': 'Cliente cadastrado com sucesso!',
            'cliente': {
                'nome': cliente.nome,
                'cpf': cliente.cpf,
                'endereco': cliente.endereco
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/conta', methods=['POST'])
def criar_conta():
    """API para criar uma nova conta"""
    try:
        data = request.json
        saldo_inicial = float(data.get('saldoInicial', 0))
        
        if data['tipo'] == 'corrente':
            conta = banco.criar_conta_corrente(
                cpf=data['cpf'],
                limite=1000,  # valor padrão
                saldo_inicial=saldo_inicial
            )
        else:  # conta poupança
            conta = banco.criar_conta_poupanca(
                cpf=data['cpf'],
                taxa_juros=0.005,  # valor padrão
                saldo_inicial=saldo_inicial
            )

        return jsonify({
            'message': 'Conta criada com sucesso!',
            'conta': {
                'numero': conta.numero,
                'tipo': conta.tipo_conta(),
                'saldo': conta.saldo,
                'cliente': {
                    'nome': conta.cliente.nome,
                    'cpf': conta.cliente.cpf
                }
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/operacao', methods=['POST'])
def realizar_operacao():
    """API para realizar operações bancárias"""
    try:
        data = request.json
        conta = banco.buscar_conta(data['numeroConta'])
        
        if data['operacao'] == 'deposito':
            valor = float(data['valor'])
            if conta.depositar(valor):
                return jsonify({
                    'message': 'Depósito realizado com sucesso!',
                    'saldo': conta.saldo
                })
            return jsonify({'error': 'Valor de depósito inválido'}), 400
            
        elif data['operacao'] == 'saque':
            valor = float(data['valor'])
            if conta.sacar(valor):
                return jsonify({
                    'message': 'Saque realizado com sucesso!',
                    'saldo': conta.saldo
                })
            return jsonify({'error': 'Saldo insuficiente ou valor inválido'}), 400
            
        elif data['operacao'] == 'extrato':
            extrato = conta.extrato()
            return jsonify({
                'extrato': extrato,
                'saldo_atual': conta.saldo
            })
            
        else:
            return jsonify({'error': 'Operação não reconhecida'}), 400
            
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/cliente/<cpf>/contas', methods=['GET'])
def listar_contas_cliente(cpf):
    """API para listar contas de um cliente"""
    try:
        contas = banco.listar_contas_cliente(cpf)
        contas_info = [{
            'numero': conta.numero,
            'tipo': conta.tipo_conta(),
            'saldo': conta.saldo
        } for conta in contas]
        
        return jsonify({
            'cpf': cpf,
            'contas': contas_info
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/conta/<numero>/saldo', methods=['GET'])
def consultar_saldo(numero):
    """API para consultar saldo de uma conta"""
    try:
        conta = banco.buscar_conta(numero)
        return jsonify({
            'numero': conta.numero,
            'tipo': conta.tipo_conta(),
            'saldo': conta.saldo
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True)
