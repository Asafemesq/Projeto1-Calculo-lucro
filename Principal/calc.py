"""Funções de cálculo de lucro e métricas relacionadas.

Este módulo não deve executar I/O em nível global para permitir importação segura
por outros módulos (por exemplo, `cli.py`).
"""

def calcular_lucro(preco_de_compra, preco_de_venda):
    """Retorna uma tupla (lucro, margem_de_lucro).

    margem_de_lucro é None se preco_de_compra for zero.
    """
    lucro = preco_de_venda - preco_de_compra
    margem_de_lucro = None
    if preco_de_compra != 0:
        margem_de_lucro = (lucro / preco_de_compra) * 100
    return lucro, margem_de_lucro


def calcular_markup(preco_de_compra, preco_de_venda):
    """Retorna o markup (preco_de_venda / preco_de_compra) ou None se inválido."""
    if preco_de_compra == 0:
        return None
    return preco_de_venda / preco_de_compra


def calcular_ponto_equilibrio(preco_de_compra, preco_de_venda):
    """Calcula o ponto de equilíbrio; retorna None se divisao por zero."""
    diferenca = preco_de_venda - preco_de_compra
    if diferenca == 0:
        return None
    return preco_de_compra / diferenca