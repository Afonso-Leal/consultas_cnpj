from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
import re

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend
db = Database()


def validar_cnpj(cnpj):
    """Valida e formata CNPJ"""
    # Remove caracteres não numéricos
    #cnpj = re.sub(r'[^0-9]', '', cnpj)

    # Verifica se tem 14 dígitos
    #if len(cnpj) != 14:
    #    return None, "CNPJ deve ter 14 dígitos"

    # Formata para exibição
    #cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

    return cnpj#, cnpj_formatado


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        'status': 'ok',
        'mensagem': 'API de consulta CNPJ está funcionando!'
    })


@app.route('/api/consultar-cnpj', methods=['GET'])
def consultar_cnpj():
    """
    Endpoint principal para consultar CNPJ
    Uso: GET /api/consultar-cnpj?cnpj=12345678000190
    """
    cnpj_input = request.args.get('cnpj', '')

    if not cnpj_input:
        return jsonify({
            'success': False,
            'erro': 'CNPJ não fornecido'
        }), 400

    # Valida e formata o CNPJ
    #cnpj_numeros, cnpj_formatado = validar_cnpj(cnpj_input)
    cnpj_numeros = validar_cnpj(cnpj_input)

    if not cnpj_numeros:
        return jsonify({
            'success': False,
            'erro': cnpj_numeros#cnpj_formatado  # Mensagem de erro
        }), 400

    # 🔍 Consulta no banco de dados REAL
    resultado = db.consultar_cnpj(cnpj_numeros)
    testesss = resultado['dados'][0].keys()
    print(testesss)
    if resultado.get('success'):
        return jsonify({
            'success': True,
            'cnpj_consultado': cnpj_numeros,
            'dados': resultado['dados'],
            'colunas' : list(resultado['dados'][0].keys())
        })
    else:
        return jsonify({
            'success': False,
            'cnpj_consultado': cnpj_numeros,
            'mensagem': resultado.get('mensagem', 'Erro na consulta')
        }), 404

    return jsonify(resultado)


@app.route('/api/empresa/<cnpj>', methods=['GET'])
def consultar_empresa(cnpj):
    """Endpoint alternativo com CNPJ na URL"""
    return consultar_cnpj()



if __name__ == '__main__':
    print("🚀 Backend API rodando na porta 5000")
    print("📝 Endpoints disponíveis:")
    print("   - GET /api/health")
    print("   - GET /api/consultar-cnpj?cnpj=12345678000190")
    print("   - GET /api/empresa/12345678000190")
    print("   - GET /api/tabela-exemplo")
    app.run(host='0.0.0.0', port=5000, debug=True)