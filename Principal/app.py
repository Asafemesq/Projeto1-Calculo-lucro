import streamlit as st
import streamlit as st
from Principal import calc
from Principal import database
import pandas as pd
from calc import calcular_lucro, calcular_markup, calcular_ponto_equilibrio

st.set_page_config(page_title="Calculadora de Lucro", layout="centered")

st.title("Calculadora de Lucro Pessoal")
st.markdown("Preencha os campos abaixo para calcular o lucro, margem de lucro, markup e ponto de equilíbrio.")

preco_custo = st.number_input("Preço de Custo (R$):", min_value=0.0, value=0.0, step=0.01, format="%.2f")
preco_venda = st.number_input("Preço de Venda (R$):", min_value=0.0, value=0.0, step=0.01, format="%.2f")
custo_servico = st.number_input("Custo de Serviço (R$):", min_value=0.0, value=0.0, step=0.01, format="%.2f")
imposto = st.number_input("Imposto (%):", min_value=0.0, value=0.0, step=0.01, format="%.2f")

if st.button("Calcular"):
    if preco_venda < preco_custo:
        st.error("O preço de venda deve ser maior ou igual ao preço de custo.")
    else:
        # calcular_lucro retorna uma tupla (lucro, margem_de_lucro)
        lucro, margem_lucro, lucro_liquido = calcular_lucro(preco_custo, preco_venda, imposto, custo_servico)
        
        # calcular_markup retorna o fator de markup
        markup = calcular_markup(preco_custo, preco_venda)
        
        # calcular_ponto_equilibrio retorna o número de unidades
        ponto_equilibrio = calcular_ponto_equilibrio(preco_custo, preco_venda)
database.inserir_calculo(preco_custo, preco_venda, custo_servico, imposto, lucro, margem_lucro, lucro_liquido, markup, ponto_equilibrio)
        st.success(f"Lucro: R$ {lucro:.2f}")
        st.success(f"Lucro Líquido: R$ {lucro_liquido:.2f}")
       
        
        if margem_lucro is not None:
            st.success(f"Margem de Lucro: {margem_lucro:.2f}%")
        else:
            st.warning("Margem de lucro não pode ser calculada (preço de custo zero)")
        
        if markup is not None:
            st.success(f"Markup (fator): {markup:.2f}x")
        else:
            st.warning("Markup não pode ser calculado (preço de custo zero)")
        
        if ponto_equilibrio is not None:
            st.info(f"Ponto de Equilíbrio: {ponto_equilibrio:.2f} unidades")
        else:
            st.warning("Ponto de equilíbrio não pode ser calculado (lucro unitário zero)")
            st.subheader("Histórico de Cálculos")
        historico = database.obter_historico_calculos(limite=5)
        if historico:
            df_historico = pd.DataFrame(historico, columns=[
                "ID", "Data", "Preço de Custo", "Preço de Venda", "Custo de Serviço",
                "Imposto (%)", "Lucro", "Margem de Lucro (%)", "Lucro Líquido",
                "Markup (fator)", "Ponto de Equilíbrio (unidades)"
            ])
            st.dataframe(df_historico)