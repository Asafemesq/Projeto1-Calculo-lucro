import streamlit as st
from calc import calcular_lucro, calcular_markup, calcular_ponto_equilibrio
st.set_page_config(page_title="Calculadora de Lucro", layout="centered")

st.title("Calculadora de Lucro Pessoal")
st.markdown("Preencha os campos abaixo para calcular o lucro, margem de lucro, markup e ponto de equilíbrio.")
preco_custo = st.number_input("Preço de Custo (R$):", min_value=0.0, value=0.0, step=0.01, format="%.2f")
preco_venda = st.number_input("Preço de Venda (R$):", min_value=0.0, value=0.0, step=0.01, format="%.2f")
if st.button("Calcular"):
    if preco_venda < preco_custo:
        st.error("O preço de venda deve ser maior ou igual ao preço de custo.")
    else:
        lucro = calcular_lucro(preco_custo, preco_venda)
        margem_lucro = calcular_markup(preco_custo, preco_venda)
        ponto_equilibrio = calcular_ponto_equilibrio(preco_custo, preco_venda)

        st.success(f"Lucro: R$ {lucro:.2f}")
        st.success(f"Margem de Lucro: {margem_lucro:.2f}%")
        st.success(f"Ponto de Equilíbrio: R$ {ponto_equilibrio:.2f}")