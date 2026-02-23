import os
import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    def __init__(self):
        self.connection_params = {
            #'host': 'cnpj-data-pipeline',
            'host': 'localhost',
            'port': '5435',
            'database': 'cnpj',
            'user': 'postgres',
            'password': 'postgres'
        }

    def get_connection(self):
        """Retorna uma conexão com o banco"""
        try:
            conn = psycopg2.connect(**self.connection_params)
            return conn
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return None

    def consultar_cnpj(self, cnpj):
        """
        Consulta um CNPJ na tabela apropriada
        Ajuste esta função conforme sua estrutura de tabelas
        """
        conn = self.get_connection()
        if not conn:
            return {'erro': 'Não foi possível conectar ao banco'}

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute(f"SELECT * FROM empresas WHERE cnpj_basico = '{cnpj}'")

            resultado = cur.fetchall()
            cur.close()
            conn.close()

            if resultado:
                return {'success': True, 'dados': resultado}
            else:
                return {'success': False, 'mensagem': 'CNPJ não encontrado'}

        except Exception as e:
            return {'erro': str(e)}

    def get_tabela_exemplo(self):
        """
        Retorna dados de exemplo para demonstração
        """
        return {
            'colunas': ['cnpj', 'razao_social', 'nome_fantasia', 'situacao', 'cidade', 'uf'],
            'dados': [
                {
                    'cnpj': '12.345.678/0001-90',
                    'razao_social': 'EMPRESA EXEMPLO LTDA',
                    'nome_fantasia': 'Exemplo Comércio',
                    'situacao': 'ATIVA',
                    'cidade': 'São Paulo',
                    'uf': 'SP'
                },
                {
                    'cnpj': '98.765.432/0001-10',
                    'razao_social': 'TECNOLOGIA EXEMPLO SA',
                    'nome_fantasia': 'TecExemplo',
                    'situacao': 'ATIVA',
                    'cidade': 'Rio de Janeiro',
                    'uf': 'RJ'
                },
                {
                    'cnpj': '11.222.333/0001-44',
                    'razao_social': 'SERVIÇOS EXEMPLO ME',
                    'nome_fantasia': 'ServExemplo',
                    'situacao': 'BAIXADA',
                    'cidade': 'Belo Horizonte',
                    'uf': 'MG'
                }
            ]
        }