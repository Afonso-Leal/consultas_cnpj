// Configurações
const API_BASE_URL = 'http://localhost:5000/api';  // Usando proxy do Nginx

// Estado da aplicação
let historicoConsultas = JSON.parse(localStorage.getItem('historico_cnpj')) || [];

// Elementos DOM
const cnpjInput = document.getElementById('cnpj-input');
const btnConsultar = document.getElementById('btn-consultar');
const loading = document.getElementById('loading');
const mensagem = document.getElementById('mensagem');
const resultados = document.getElementById('resultados');
const tabelaContainer = document.getElementById('tabela-container');
const cnpjConsultado = document.getElementById('cnpj-consultado');
const historicoDiv = document.getElementById('historico');
const listaHistorico = document.getElementById('lista-historico');

// Formata CNPJ enquanto digita
cnpjInput.addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');

    if (value.length <= 14) {
        value = value.replace(/^(\d{2})(\d)/, '$1.$2');
        value = value.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
        value = value.replace(/\.(\d{3})(\d)/, '.$1/$2');
        value = value.replace(/(\d{4})(\d)/, '$1-$2');

        e.target.value = value;
    }
});

// Evento de consulta
btnConsultar.addEventListener('click', consultarCNPJ);
cnpjInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        consultarCNPJ();
    }
});

// Função principal de consulta
async function consultarCNPJ() {
    const cnpj = cnpjInput.value.trim();

    if (!cnpj) {
        mostrarMensagem('Por favor, digite um CNPJ', 'erro');
        return;
    }

    // Mostra loading
    loading.style.display = 'flex';
    mensagem.style.display = 'none';
    resultados.style.display = 'none';

    try {
        // Remove caracteres especiais para enviar à API
        const cnpjNumeros = cnpj.replace(/\D/g, '');

        // Faz requisição à API
        const response = await fetch(`${API_BASE_URL}/consultar-cnpj?cnpj=${cnpjNumeros}`);
        const data = await response.json();

        // Esconde loading
        loading.style.display = 'none';

        if (data.success) {
            // Mostra resultado
            mostrarResultado(data);
            adicionarAoHistorico(cnpj);
        } else {
            mostrarMensagem(data.mensagem || 'CNPJ não encontrado', 'erro');
        }
    } catch (error) {
        console.error('Erro na consulta:', error);
        loading.style.display = 'none';
        mostrarMensagem('Erro ao consultar API. Verifique se o backend está rodando.', 'erro');
    }
}

// Mostra o resultado em tabela
function mostrarResultado(data) {
    // Mostra o CNPJ consultado
    cnpjConsultado.textContent = `CNPJ: ${data.cnpj_consultado || 'N/A'}`;

    // Cria a tabela
    if (data.dados && data.dados.length > 0) {
        const tabela = document.createElement('table');

        // Cabeçalho
        if (data.colunas) {
            const thead = document.createElement('thead');
            const tr = document.createElement('tr');

            data.colunas.forEach(coluna => {
                const th = document.createElement('th');
                th.textContent = coluna.toUpperCase().replace('_', ' ');
                tr.appendChild(th);
            });
            thead.appendChild(tr);
            tabela.appendChild(thead);
        }

        // Corpo da tabela
        const tbody = document.createElement('tbody');
        data.dados.forEach(item => {
            const tr = document.createElement('tr');
            if (data.colunas) {
                data.colunas.forEach(coluna => {
                    const td = document.createElement('td');
                    td.textContent = item[coluna] || '-';
                    tr.appendChild(td);
                });
            } else {
                // Se não tem colunas definidas, mostra todas as chaves
                Object.values(item).forEach(valor => {
                    const td = document.createElement('td');
                    td.textContent = valor || '-';
                    tr.appendChild(td);
                });
            }
            tbody.appendChild(tr);
        });
        tabela.appendChild(tbody);

        // Limpa e adiciona nova tabela
        tabelaContainer.innerHTML = '';
        tabelaContainer.appendChild(tabela);
    } else {
        tabelaContainer.innerHTML = '<p>Nenhum dado encontrado</p>';
    }

    // Mostra resultados
    resultados.style.display = 'block';
    mensagem.style.display = 'none';
}

// Mostra mensagem para o usuário
function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem ${tipo}`;
    mensagem.style.display = 'block';
    resultados.style.display = 'none';
}

// Adiciona ao histórico
function adicionarAoHistorico(cnpj) {
    if (!historicoConsultas.includes(cnpj)) {
        historicoConsultas.unshift(cnpj);
        if (historicoConsultas.length > 5) {
            historicoConsultas.pop();
        }
        localStorage.setItem('historico_cnpj', JSON.stringify(historicoConsultas));
        atualizarHistorico();
    }
}

// Atualiza exibição do histórico
function atualizarHistorico() {
    if (historicoConsultas.length > 0) {
        historicoDiv.style.display = 'block';
        listaHistorico.innerHTML = '';

        historicoConsultas.forEach(cnpj => {
            const li = document.createElement('li');
            li.textContent = cnpj;
            li.addEventListener('click', () => {
                cnpjInput.value = cnpj;
                consultarCNPJ();
            });
            listaHistorico.appendChild(li);
        });
    } else {
        historicoDiv.style.display = 'none';
    }
}

// Verifica saúde da API ao carregar
async function verificarAPI() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            mostrarMensagem('✅ Conectado à API', 'sucesso');
        } else {
            mostrarMensagem('⚠️ API não respondeu corretamente', 'erro');
        }
    } catch (error) {
        mostrarMensagem('❌ Não foi possível conectar à API. Verifique se o backend está rodando.', 'erro');
    }
}

// Inicialização
atualizarHistorico();
verificarAPI();

// Atualiza a cada 30 segundos
setInterval(verificarAPI, 30*10000);