import streamlit as st
import pandas as pd

# Importações relativas (mesmo pacote)
from calc import calcular_lucro, calcular_markup, calcular_ponto_equilibrio
import database

# Inicializar banco de dados
database.criar_tabela()

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
        # Cálculos básicos (agora retorna 4 valores)
        lucro, margem_bruta, lucro_liquido, margem_liquida = calcular_lucro(preco_custo, preco_venda, imposto, custo_servico)
        markup = calcular_markup(preco_custo, preco_venda)
        ponto_equilibrio = calcular_ponto_equilibrio(preco_custo, preco_venda)
        
        # Salvar no banco de dados
        database.salvar_registro(
            preco_custo, 
            preco_venda, 
            lucro, 
            margem_bruta if margem_bruta is not None else 0.0,
            custo_servico, 
            imposto, 
            lucro_liquido
        )
        
        # Exibir resultados principais
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("💰 Lucro Bruto", f"R$ {lucro:.2f}")
            st.metric("💵 Lucro Líquido", f"R$ {lucro_liquido:.2f}", 
                     delta=f"{lucro_liquido - lucro:.2f}" if lucro != lucro_liquido else None)
        
        with col2:
            if margem_bruta is not None:
                st.metric("📊 Margem Bruta", f"{margem_bruta:.2f}%", 
                         help="Lucro bruto sobre o custo")
            
            if margem_liquida is not None:
                # Indicador visual de margem saudável
                cor = "🟢" if margem_liquida >= 20 else "🟡" if margem_liquida >= 10 else "🔴"
                st.metric(f"{cor} Margem Líquida", f"{margem_liquida:.2f}%",
                         help="Lucro líquido sobre a venda (mais preciso para tomada de decisão)")
        
        st.divider()
        
        # Métricas adicionais
        if markup is not None:
            st.info(f"🔢 Markup (fator): **{markup:.2f}x** - Você multiplica o custo por {markup:.2f} para chegar ao preço de venda")
        else:
            st.warning("Markup não pode ser calculado (preço de custo zero)")
        
        if ponto_equilibrio is not None:
            st.info(f"⚖️ Ponto de Equilíbrio: **{ponto_equilibrio:.0f} unidades** - Você precisa vender {ponto_equilibrio:.0f} unidades para cobrir os custos")
        else:
            st.warning("Ponto de equilíbrio não pode ser calculado (lucro unitário zero ou negativo)")

# Exibir histórico
st.divider()
st.subheader("Histórico de Cálculos (Últimos 10 registros)")
historico = database.obter_historico()

if historico:
    # Inverter para mostrar os mais recentes primeiro
    historico_recente = historico[-10:][::-1]
    
    df_historico = pd.DataFrame(historico_recente, columns=[
        "ID", "Data", "Preço de Custo", "Preço de Venda", "Lucro Bruto", 
        "Margem de Lucro (%)", "Custo de Serviço", "Imposto (%)", "Lucro Líquido"
    ])
    
    # Formatar valores monetários
    colunas_moeda = ["Preço de Custo", "Preço de Venda", "Lucro Bruto", "Custo de Serviço", "Lucro Líquido"]
    for col in colunas_moeda:
        df_historico[col] = df_historico[col].apply(lambda x: f"R$ {x:.2f}")
    
    df_historico["Margem de Lucro (%)"] = df_historico["Margem de Lucro (%)"].apply(lambda x: f"{x:.2f}%")
    df_historico["Imposto (%)"] = df_historico["Imposto (%)"].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(df_historico, use_container_width=True)
else:
    st.info("Nenhum cálculo realizado ainda.")