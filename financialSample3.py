import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análise Financeira", layout="wide")
st.title("📊 Dashboard Financeiro - Microsoft Sample")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("MS_Financial_Sample.csv", on_bad_lines='skip')
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Year"] = df["Date"].dt.year  # Garante que a coluna Year existe como datetime
    df.dropna(inplace=True)
    return df

df = carregar_dados()

with st.sidebar:
    st.header("🔍 Filtros")
    anos = st.multiselect("Ano", options=sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
    segmentos = st.multiselect("Segmento", options=sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique()))
    paises = st.multiselect("País", options=sorted(df["Country"].unique()), default=sorted(df["Country"].unique()))

df_filtrado = df[
    (df["Year"].isin(anos)) &
    (df["Segment"].isin(segmentos)) &
    (df["Country"].isin(paises))
]

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("📈 Receita Total", f"${df_filtrado['Revenue'].sum():,.2f}")
col2.metric("💰 Lucro Total", f"${df_filtrado['Profit'].sum():,.2f}")
col3.metric("📦 Unidades Vendidas", f"{int(df_filtrado['Units Sold'].sum()):,}")

st.markdown("---")

# Tabela: Lucro por Segmento
st.subheader("🏢 Lucro por Segmento")
df_lucro_segmento = df_filtrado.groupby("Segment")["Profit"].sum().reset_index()
st.dataframe(df_lucro_segmento.style.format({"Profit": "${:,.2f}"}))

# Tabela: Lucro por Produto
st.subheader("📦 Lucro por Produto")
df_lucro_produto = df_filtrado.groupby(["Product", "Segment"])["Profit"].sum().reset_index()
st.dataframe(df_lucro_produto.style.format({"Profit": "${:,.2f}"}))

# Tabela: Receita, Lucro e Unidades por Produto
st.subheader("📍 Receita e Lucro por Produto")
df_receita_lucro = df_filtrado.groupby(["Product", "Segment"])[["Revenue", "Profit", "Units Sold"]].sum().reset_index()
st.dataframe(df_receita_lucro.style.format({
    "Revenue": "${:,.2f}",
    "Profit": "${:,.2f}",
    "Units Sold": "{:,}"
}))

st.markdown("---")

# ========================
# GRÁFICOS SIMPLES (streamlit nativo)
# ========================
st.subheader("📊 Gráficos Simples")

# 1. Lucro por Ano
df_lucro_ano = df_filtrado.groupby("Year")["Profit"].sum()
st.write("💰 Lucro Total por Ano")
st.bar_chart(df_lucro_ano)

# 2. Vendas por Segmento
df_vendas_segmento = df_filtrado.groupby("Segment")["Sales"].sum()
st.write("🧩 Vendas Totais por Segmento")
st.bar_chart(df_vendas_segmento)

# 3. Top 5 Produtos Mais Lucrativos
df_lucro_prod_top5 = df_filtrado.groupby("Product")["Profit"].sum().sort_values(ascending=False).head(5)
st.write("⭐ Top 5 Produtos Mais Lucrativos")
st.bar_chart(df_lucro_prod_top5)
