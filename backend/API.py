# web/app.py
import os
import time
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Configurações do banco via variáveis de ambiente [citation:9]



def get_db_connection():
    """Função para conectar ao banco com retry"""
    max_retries = 1
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            print("✅ Conectado ao PostgreSQL com sucesso!")
            return conn
        except psycopg2.OperationalError as e:
            print(f"⚠️  Tentativa {attempt + 1}/{max_retries} falhou: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Aguardando {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                print("❌ Não foi possível conectar ao banco após várias tentativas")
                raise


@app.route('/')
def home():
    return jsonify({
        'message': '🚀 Aplicação rodando com Docker!',
        'status': 'connected to DB' if check_db_connection() else 'DB connection failed'
    })


@app.route('/cnpj/<val_cnpj>', methods=['GET'])
def get_cnpj(val_cnpj):
    """Exemplo de consulta ao banco"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        conn.commit()

        # Busca um usuario (exemplo)
        cur.execute(f"SELECT * FROM empresas WHERE cnpj_basico = '{val_cnpj}'")
        users = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            'users': [
                {'razao_social': u[0]}
                for u in users
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def check_db_connection():
    try:
        conn = get_db_connection()
        conn.close()
        return True
    except:
        return False


if __name__ == '__main__':
    # Aguarda o banco ficar disponível
    print("⏳ Aguardando conexão com o banco de dados...")
    time.sleep(3)  # Pequena pausa inicial

    try:
        get_db_connection()
    except:
        raise
    app.run(host='0.0.0.0', port=8000, debug=True)