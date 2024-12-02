import streamlit as st
import importlib
# Configuração da página do Streamlit
st.set_page_config(layout="wide")

# Importação de bibliotecas
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime
from datetime import date
from PIL import Image
import folium
from streamlit_folium import folium_static
import os

import pandas as pd

# Caminho relativo (mesmo diretório do script)
file_path = "train.csv"
df = pd.read_csv(file_path)


# Limpeza do dataset:
# 1. Convertendo a coluna 'Delivery_person_Age' de texto para número
df1 = df.copy()
df1 = df1[df1['Delivery_person_Age'] != 'NaN ']
df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

# Filtrando valores 'NaN' em outras colunas
df1 = df1[df1['City'] != 'NaN ']
df1 = df1[df1['Festival'] != 'NaN ']
df1 = df1[df1['Road_traffic_density'] != 'NaN ']

# 2. Convertendo a coluna 'Delivery_person_Ratings' de texto para número decimal (float)
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

# 3. Convertendo a coluna 'Order_Date' de texto para data
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

# 4. Convertendo 'multiple_deliveries' de texto para número inteiro (int)
df1 = df1[df1['multiple_deliveries'] != 'NaN ']
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

# 5. Aplicando strip() em todas as colunas de texto
df1 = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Remover a parte '(min)' das strings na coluna 'Time_taken(min)'
df1['Time_taken(min)'] = df1['Time_taken(min)'].str.replace(r'\(min\)', '', regex=True)

# Converter para int
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

#===================================================
# Barra lateral
#===================================================

st.header('Marketplace - Visão Empresa')

# Exibindo imagem no sidebar
image_path = 'logo.jpg'
image = Image.open(image_path)
st.sidebar.image(image, width=220)

# Sidebar
st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

# Selecione uma data limite
st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13).date(),  # Data padrão
    min_value=datetime(2022, 2, 11).date(),  # Data mínima
    max_value=datetime(2022, 4, 6).date(),  # Data máxima
    format='YYYY-MM-DD'  # O formato de exibição
)

# Convertendo a data do slider para datetime64[ns] para compatibilidade
date_slider = pd.to_datetime(date_slider)

# Filtro de condições do trânsito
st.sidebar.markdown("""---""")
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)

st.sidebar.markdown("""---""")
st.sidebar.markdown('### @Powered by Vitor Campos Moura Costa')

# Aplicando os filtros
df1 = df1[df1['Order_Date'] < date_slider]
df1 = df1[df1['Road_traffic_density'].isin(traffic_options)]

# Função para carregar o dashboard baseado na opção escolhida
def load_dashboard(dashboard_name):
    if dashboard_name == "visao_empresa":
        module = importlib.import_module("visao_empresa")
        module.run_dashboard()
    elif dashboard_name == "visao_entregadores":
        module = importlib.import_module("visao_entregadores")
        module.run_dashboard()
    elif dashboard_name == "visao_restaurantes":
        module = importlib.import_module("visao_restaurantes")
        module.run_dashboard()

# Título principal da aplicação
st.title("Análises da Empresa Curry Company")

# Menu de navegação entre os dashboards
dashboard_name = st.sidebar.radio(
    "Escolha o Dashboard:",
    ("visao_empresa", "visao_entregadores", "visao_restaurantes")
)

# Carregar o dashboard escolhido
load_dashboard(dashboard_name)
