# Usuario e calculo
# Seção 1: importação de módulos
from .calc import (
    calcular_lucro,
    calcular_markup,
    calcular_ponto_equilibrio,
)

# Seção 2: funções auxiliares
def obter_entrada_numerica(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0:
                print("Por favor, insira um número positivo.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")


def exibir_resultados_lucro(lucro, margem_de_lucro, markup=None, ponto_equilibrio=None):
    """Exibe o resultado do cálculo de lucro formatado, incluindo markup e ponto de equilíbrio."""
    print("\nResultados do Cálculo:")
    print(f"Lucro Absoluto: {lucro:.2f}")
    if margem_de_lucro is not None:
        print(f"Margem de Lucro: {margem_de_lucro:.2f}%")
    else:
        print("Margem de lucro não pode ser calculada devido ao preço de compra ser zero.")

    if markup is not None:
        print(f"Markup (fator): {markup:.2f}")
    else:
        print("Markup não pode ser calculado devido ao preço de compra ser zero.")

    if ponto_equilibrio is not None:
        print(f"Ponto de Equilíbrio (unidades): {ponto_equilibrio:.2f}")
    else:
        print("Ponto de equilíbrio não pode ser calculado devido a divisão por zero.")

# Seção 3: Função principal da interface
def executar_calculadora_lucro():
    print("Bem-vindo à Calculadora de Lucro!\n")
    preco_de_compra = obter_entrada_numerica("Digite o preço de compra: R$ ")
    preco_de_venda = obter_entrada_numerica("Digite o preço de venda: R$ ")

    lucro, margem_de_lucro = calcular_lucro(preco_de_compra, preco_de_venda)
    markup = calcular_markup(preco_de_compra, preco_de_venda)
    ponto_equilibrio = calcular_ponto_equilibrio(preco_de_compra, preco_de_venda)
    exibir_resultados_lucro(lucro, margem_de_lucro, markup=markup, ponto_equilibrio=ponto_equilibrio)

    # Seção 4: Execução do programa
if __name__ == "__main__":
    executar_calculadora_lucro()