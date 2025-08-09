// Função para mostrar/esconder seções
function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.add('hidden');
    });
    document.getElementById(sectionId).classList.remove('hidden');
}

// Função para mostrar mensagem de erro ou sucesso
function showMessage(message, isError = false) {
    const resultado = document.getElementById('resultado');
    const conteudoResultado = document.getElementById('conteudoResultado');
    
    resultado.classList.remove('hidden');
    conteudoResultado.innerHTML = `
        <div class="${isError ? 'error' : 'success'}">
            ${message}
        </div>
    `;
}

// Event Listeners para os formulários
document.getElementById('clienteForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        nome: document.getElementById('nome').value,
        cpf: document.getElementById('cpf').value,
        endereco: document.getElementById('endereco').value
    };

    // Aqui você faria a chamada para o backend
    console.log('Cadastrando cliente:', data);
    showMessage('Cliente cadastrado com sucesso!');
    this.reset();
});

document.getElementById('contaForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        cpf: document.getElementById('cpfConta').value,
        tipo: document.getElementById('tipoConta').value,
        saldoInicial: document.getElementById('saldoInicial').value
    };

    // Aqui você faria a chamada para o backend
    console.log('Criando conta:', data);
    showMessage('Conta criada com sucesso!');
    this.reset();
});

document.getElementById('operacoesForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const operacao = document.getElementById('tipoOperacao').value;
    const data = {
        numeroConta: document.getElementById('numeroConta').value,
        operacao: operacao,
        valor: document.getElementById('valor').value
    };

    // Aqui você faria a chamada para o backend
    console.log('Executando operação:', data);
    showMessage(`Operação de ${operacao} realizada com sucesso!`);
});

// Mostrar/esconder campo de valor conforme o tipo de operação
document.getElementById('tipoOperacao').addEventListener('change', function() {
    const valorGroup = document.getElementById('valorGroup');
    valorGroup.style.display = this.value === 'extrato' ? 'none' : 'block';
});

// Inicializar mostrando a seção de clientes
document.addEventListener('DOMContentLoaded', function() {
    showSection('cliente');
});
