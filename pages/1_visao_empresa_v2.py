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

# Funções de Limpeza e Pré-processamento de Dados
def cleancode(df):
    """
    Função de limpeza do DataFrame:
    - Remoção de valores NaN
    - Conversão de tipos de dados
    - Remoção de espaços em colunas de texto
    - Formatação de datas e tempos
    """
    df1 = df.copy()
    
    # Limpeza e conversão de colunas
    df1 = df1[df1['Delivery_person_Age'] != 'NaN ']
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1 = df1[df1['City'] != 'NaN ']
    df1 = df1[df1['Festival'] != 'NaN ']
    df1 = df1[df1['Road_traffic_density'] != 'NaN ']
    
    # Conversões adicionais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    # Limpeza de outras colunas
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int, errors='ignore')
    df1 = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.replace(r'\(min\)', '', regex=True)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1

# Funções de Visualização
def order_metric(df1):
    """ Gera gráfico de barras: quantidade de pedidos por data """
    cols = ['ID', 'Order_Date']
    selecao = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
    fig = px.bar(selecao, x='Order_Date', y='ID')
    return fig

def traffic_order_share(df1):
    """ Gera gráfico de pizza: distribuição percentual de pedidos por tráfego """
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum() * 100
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
    return fig

def traffic_order_city(df1):
    """ Gera gráfico de dispersão: pedidos por cidade e tráfego """
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig

def order_by_week(df1):
    """ Gera gráfico de linha: pedidos por semana """
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    qtd_semana = df1.loc[:, ['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index()
    fig = px.line(qtd_semana, x='Week_of_year', y='ID')
    return fig

def order_share_by_week(df1):
    """ Gera gráfico de linha: pedidos por entregador por semana """
    df_aux1 = df1.loc[:, ['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby('Week_of_year')['Delivery_person_ID'].nunique().reset_index()
    df_aux = pd.merge(df_aux1, df_aux2, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x='Week_of_year', y='order_by_deliver')
    return fig

# Funções de Mapas
def country_maps(df1):
    """ Gera mapa interativo com localizações de entregas e informações de tráfego """
    df_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
              .groupby(['City', 'Road_traffic_density'])
              .median()
              .reset_index())
    
    map = folium.Map()
    
    for index, location_info in df_aux.iterrows():
        folium.Marker(
            [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']],
            popup=f"City: {location_info['City']}<br>Traffic: {location_info['Road_traffic_density']}"
        ).add_to(map)
    
    folium_static(map, width=700, height=350)

# Funções de Interface com o Usuário (Streamlit)
def sidebar():
    """ Função para criar a barra lateral no Streamlit """
    st.header('Marketplace - Visão Empresa')

    # Exibindo imagem no sidebar
    image_path = 'logo.jpg'
    image = Image.open(image_path)
    st.sidebar.image(image, width=220)

    # Sidebar título e descrição
    st.sidebar.markdown('# Curry Company')
    st.sidebar.markdown('## Fastest Delivery in Town')
    st.sidebar.markdown("""---""")

    # Filtro de data
    st.sidebar.markdown('## Selecione uma data limite')
    date_slider = st.sidebar.slider(
        'Até qual valor?',
        value=datetime(2022, 4, 13).date(),
        min_value=datetime(2022, 2, 11).date(),
        max_value=datetime(2022, 4, 6).date(),
        format='YYYY-MM-DD'
    )
    return pd.to_datetime(date_slider)

def main(df):
    """ Função principal para rodar a aplicação Streamlit """
    # Limpeza dos dados
    df1 = cleancode(df)

    # Filtros na barra lateral
    date_slider = sidebar()
    
    # Aplicando o filtro de data
    df1 = df1[df1['Order_Date'] < date_slider]

    # Títulos para as abas
    tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Estratégica', 'Visão Geográfica'])

    with tab1:
        with st.container():
            # Pedidos Diários
            st.markdown('# Pedidos Diários')
            fig = order_metric(df1)       
            st.plotly_chart(fig, use_container_width=True)

        # Pedidos X Tráfego e Pedidos por Cidade e Tráfego
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('### Pedidos X Tráfego')
                fig = traffic_order_share(df1)
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                st.markdown('### Pedidos por Cidade e Tráfego')
                fig = traffic_order_city(df1)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Pedidos por Semana
        with st.container():
            st.markdown("# Pedidos por Semana")
            fig = order_by_week(df1)
            st.plotly_chart(fig, use_container_width=True)

        # Pedidos por Semana por Entregador
        with st.container():
            st.markdown('# Order by Week')
            fig = order_share_by_week(df1)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Localização por Tráfego
        st.markdown("# Localização por Tráfego")
        country_maps(df1)

# Código para rodar a aplicação
if __name__ == "__main__":
    # Importar o dataset
    file_path = "train.csv"
    df = pd.read_csv(file_path)
    
    # Rodar a função principal
    main(df)