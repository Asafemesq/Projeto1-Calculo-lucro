import sqlite3
from datetime import datetime
import os

DATABASE_FILE = "lucro_calculadora.db"

def criar_tabela():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            preco_custo REAL,
            preco_venda REAL,
            lucro REAL,
            margem_lucro REAL,
            custo_servico REAL,
            imposto_percentual REAL,
            lucro_liquido REAL
        )
    """)
    conn.commit()
    conn.close()

def salvar_registro(preco_custo, preco_venda, lucro, margem_lucro, custo_servico, imposto_percentual, lucro_liquido):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historico (data, preco_custo, preco_venda, lucro, margem_lucro, custo_servico, imposto_percentual, lucro_liquido)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), preco_custo, preco_venda, lucro, margem_lucro, custo_servico, imposto_percentual, lucro_liquido))
    conn.commit()
    conn.close()
def obter_historico():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM historico")
    registros = cursor.fetchall()
    conn.close()
    return registros
