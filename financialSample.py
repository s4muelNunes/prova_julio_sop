import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análise Financeira", layout="wide")
st.title("📊 Dashboard Financeiro - Microsoft Sample")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("MS_Financial_Sample.csv", on_bad_lines='skip')
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.dropna(inplace=True)
    return df

df = carregar_dados()

with st.sidebar:
    st.header("🔍 Filtros")
    anos = st.multiselect("Ano", options=sorted(df["year"].unique()), default=sorted(df["year"].unique()))
    segmentos = st.multiselect("Segmento", options=sorted(df["segment"].unique()), default=sorted(df["segment"].unique()))
    paises = st.multiselect("País", options=sorted(df["country"].unique()), default=sorted(df["country"].unique()))

df_filtrado = df[
    (df["year"].isin(anos)) &
    (df["segment"].isin(segmentos)) &
    (df["country"].isin(paises))
]

col1, col2, col3 = st.columns(3)
col1.metric("📈 Receita Total", f"${df_filtrado['revenue'].sum():,.2f}")
col2.metric("💰 Lucro Total", f"${df_filtrado['profit'].sum():,.2f}")
col3.metric("📦 Unidades Vendidas", f"{int(df_filtrado['units_sold'].sum()):,}")

st.markdown("---")

st.subheader("🏢 Lucro por Segmento")
df_lucro_segmento = df_filtrado.groupby("segment")["profit"].sum().reset_index()
st.dataframe(df_lucro_segmento.style.format({"profit": "${:,.2f}"}))

st.subheader("📦 Lucro por Produto")
df_lucro_produto = df_filtrado.groupby(["product", "segment"])["profit"].sum().reset_index()
st.dataframe(df_lucro_produto.style.format({"profit": "${:,.2f}"}))

st.subheader("📍 Receita e Lucro por Produto")
df_receita_lucro = df_filtrado.groupby(["product", "segment"])[["revenue", "profit", "units_sold"]].sum().reset_index()
st.dataframe(df_receita_lucro.style.format({
    "revenue": "${:,.2f}",
    "profit": "${:,.2f}",
    "units_sold": "{:,}"
}))
