# 📊 Projeto – Análise de Salários em Dados (Imersão Alura + Dashboard)

Este projeto teve como objetivo analisar salários da área de tecnologia a partir de um dataset internacional com mais de **133 mil registros**. A execução envolveu todo o processo de **ETL (Extração, Transformação e Limpeza de Dados)** e a criação de visualizações interativas.  

---

## 🔧 Principais etapas desenvolvidas
- **Coleta e Tratamento de Dados**  
  - Importação dos dados via Google Colab utilizando **Pandas** e **NumPy**  
  - Renomeação e padronização de colunas  
  - Tradução e categorização de variáveis (nível de experiência, tipo de contrato, porte da empresa e modelo de trabalho)  
  - Exclusão e tratamento de valores nulos e conversão de tipos  

- **Análise Exploratória de Dados (EDA)**  
  - Estatísticas descritivas sobre salários, níveis de senioridade e localizações  
  - Visualizações com **Matplotlib** e **Seaborn** (distribuição, boxplots e comparativos de médias)  
  - Gráficos interativos com **Plotly** (barras, pizza e comparativos por país e tipo de trabalho)  

- **Dashboard Interativo**  
  - Construído com **Streamlit** em Python  
  - Permitiu filtros dinâmicos (por ano, país, cargo e senioridade)  
  - Visualizações atualizadas em tempo real, facilitando a exploração dos dados por diferentes perspectivas  
  - 🔗 **Acesse o dashboard aqui:** [Link para o Dashboard](https://dashboard-salarios-naarea-de-dados.streamlit.app/)  

---

## 📈 Resultados Obtidos
- Identificação de padrões salariais por **nível de experiência** (Executivo > Sênior > Pleno > Júnior)  
- Comparativo entre **modelos de trabalho** (predominância presencial, mas com salários mais competitivos no remoto)  
- Diferenças salariais relevantes por **localização geográfica** e **cargo específico** (ex.: Data Scientist, Engineer, Manager)
