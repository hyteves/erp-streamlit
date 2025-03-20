import streamlit as st
import pandas as pd
import sqlite3
import datetime
from faker import Faker

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios", "Distribuição Contas a Pagar", "Top 5 Clientes", "Comparação Receita vs Despesa"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatório de Fluxo de Caixa")
        df = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos GROUP BY tipo", conn)
        st.dataframe(df)

    elif choice == "Distribuição Contas a Pagar":
        st.subheader("Distribuição das Contas a Pagar por Fornecedor")
        df = pd.read_sql_query("SELECT fornecedor, SUM(valor) as total FROM contas_pagar GROUP BY fornecedor", conn)
        df.set_index('fornecedor', inplace=True)
        st.bar_chart(df['total'])
    
    elif choice == "Top 5 Clientes":
        st.subheader("Top 5 Clientes com Maior Receita")
        df = pd.read_sql_query('''
            SELECT c.nome, SUM(cr.valor) as total_receita
            FROM contas_receber cr
            JOIN clientes c ON cr.cliente_id = c.id
            GROUP BY c.nome
            ORDER BY total_receita DESC
            LIMIT 5
        ''', conn)
        
        st.dataframe(df)

        st.bar_chart(df.set_index('nome')['total_receita'])

    elif choice == "Comparação Receita vs Despesa":
        st.subheader("Comparação Receita vs Despesa (Mês Atual)")
        current_month = datetime.datetime.now().strftime('%Y-%m')  # Pegando o mês atual
        df = pd.read_sql_query(f'''
            SELECT tipo, SUM(valor) as total
            FROM lancamentos
            WHERE strftime('%Y-%m', data) = "{current_month}"
            GROUP BY tipo
        ''', conn)

        df.set_index('tipo', inplace=True)
        st.bar_chart(df['total'])
    
    conn.close()
    
if __name__ == "__main__":
    main()
