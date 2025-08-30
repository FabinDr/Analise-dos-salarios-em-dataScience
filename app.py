import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------
# Configuração da Página
# -----------------------------
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon=("./img/icon-barra.png"),
    layout="wide",
)

# -----------------------------
# Função com cache para carregar os dados
# -----------------------------
@st.cache_data
def carregar_dados():
    return pd.read_csv("dataframeFinal.csv")

df = carregar_dados()

# -----------------------------
# Filtros - Barra lateral
# -----------------------------
st.sidebar.image("logo.svg")
st.sidebar.header("Selecione o Filtro")

anos_disponiveis = sorted(df['ano_trabalho'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione o ano", anos_disponiveis, default=anos_disponiveis)

senioridades_disponiveis = sorted(df['nivel_experiencia'].unique())
senioridades_selecionadas = st.sidebar.multiselect(
    "Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect(
    "Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

tamanhos_disponiveis = sorted(df['porte_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect(
    "Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# -----------------------------
# Filtragem do DataFrame
# -----------------------------
df_filtrado = df[
    (df['ano_trabalho'].isin(anos_selecionados)) &
    (df['nivel_experiencia'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['porte_empresa'].isin(tamanhos_selecionados))
]

# -----------------------------
# Título e descrição
# -----------------------------
st.title("Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# -----------------------------
# Métricas Principais (KPIs)
# -----------------------------
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

# -----------------------------
# Gráficos
# -----------------------------
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

# --- Gráfico 1: Top 10 cargos
with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_traces(marker_color="#154C79")
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

# --- Gráfico 2: Histograma
with col_graf2:
    if not df_filtrado.empty:
        # Amostra para não travar em datasets grandes
        df_sample = df_filtrado.sample(min(len(df_filtrado), 5000))
        grafico_hist = px.histogram(
            df_sample,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': 'Contagem'}
        )
        grafico_hist.update_traces(
            marker_color="#154C79",
            hovertemplate='Faixa: $%{x:,.0f}<br>Contagem: %{y}<extra></extra>'
        )
        grafico_hist.update_layout(
            bargap=0.2,
            title_x=0.1,
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(title='Faixa salarial (USD)', tickprefix='$', tickformat=',.0f'),
            yaxis=dict(title='Contagem'),
            template="plotly_white",
            height=420
        )
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

# --- Gráfico 3: Trabalho remoto
with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

# --- Gráfico 4: Salário por país (apenas Data Scientist)
with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        if not df_ds.empty:
            media_salarial_por_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
            grafico_paises = px.choropleth(
                media_salarial_por_pais,
                locations='residencia_iso3',
                color='usd',
                color_continuous_scale='rdylgn',
                title='Salário médio de Cientista de Dados por país',
                labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'}
            )
            grafico_paises.update_layout(title_x=0.1)
            st.plotly_chart(grafico_paises, use_container_width=True)
        else:
            st.warning("Nenhum dado de Cientistas de Dados para exibir no gráfico de países.")
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

# -----------------------------
# Tabela de Dados
# -----------------------------
st.subheader("Dados Detalhados")

with st.expander("Tabela com os Dados"):
    default_cols = list(df_filtrado.columns)
    showData = st.multiselect("Filtros de colunas:", options=df_filtrado.columns, default=default_cols)

    # Limita a exibição para não travar
    st.dataframe(df_filtrado[showData].head(200))
    st.caption(f"Mostrando até 200 de {len(df_filtrado)} registros.")

# -----------------------------
# CSS - Remove menu, footer e header
# -----------------------------
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
