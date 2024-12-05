# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime, date
import os
from PIL import Image
import numpy as np

st.set_page_config(page_title='Visão Empresa', page_icon='🍽️', layout='wide')

# Função para carregar o dataset
def load_data(file_path):
    """
    Carrega o dataset a partir de um arquivo CSV.
    """
    return pd.read_csv(file_path)

# Função para limpar o dataset
def clean_data(df):
    """
    Limpa o DataFrame, tratando NaN, convertendo colunas e removendo espaços desnecessários.
    """
    df1 = df.copy()

    # Limpeza de dados
    df1 = df1[df1['Delivery_person_Age'] != 'NaN ']
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    df1 = df1[df1['City'] != 'NaN ']
    df1 = df1[df1['Festival'] != 'NaN ']
    df1 = df1[df1['Road_traffic_density'] != 'NaN '] 

    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    df1 = df1[df1['multiple_deliveries'] != 'NaN ']
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # Aplicando strip em todas as colunas de texto
    for col in ['Delivery_person_ID', 'Type_of_order', 'Type_of_vehicle', 'City', 'ID', 
                'Road_traffic_density', 'Weatherconditions', 'Festival']:
        df1[col] = df1[col].str.strip()

    # Remover '(min)' da coluna 'Time_taken(min)'
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.replace(r'\(min\)', '', regex=True)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

# Função para exibir a barra lateral
def sidebar():
    """
    Exibe a barra lateral do Streamlit com logo, título, data e filtros.
    """
    st.sidebar.markdown('# Curry Company')
    st.sidebar.markdown('## Fastest Delivery in Town')
    st.sidebar.markdown("""---""")

    # Adicionando logo
    image_path = 'logo.jpg'
    image = Image.open(image_path)
    st.sidebar.image(image, width=220)

    # Filtro de data
    st.sidebar.markdown('## Selecione uma data limite')
    date_slider = st.sidebar.slider(
        'Até qual valor?',
        value=datetime(2022, 4, 13).date(),
        min_value=datetime(2022, 2, 11).date(),
        max_value=datetime(2022, 4, 6).date(),
        format='YYYY-MM-DD'
    )

    st.sidebar.markdown("""---""")
    
    # Filtro de condições de tráfego
    traffic_options = st.sidebar.multiselect(
        'Quais as condições do trânsito?',
        ['Low', 'Medium', 'High', 'Jam'],
        default=['Low', 'Medium', 'High', 'Jam']
    )
    
    # Créditos
    st.sidebar.markdown("""---""")
    st.sidebar.markdown('### @Powered by Vitor Campos Moura Costa')

    return pd.to_datetime(date_slider), traffic_options

# Função para aplicar os filtros
def apply_filters(df, date_slider, traffic_options):
    """
    Aplica os filtros de data e trânsito no DataFrame.
    """
    df_filtered = df[df['Order_Date'] < date_slider]
    df_filtered = df_filtered[df_filtered['Road_traffic_density'].isin(traffic_options)]
    return df_filtered

# Função para exibir as métricas gerais
def display_overall_metrics(df):
    """
    Exibe as métricas gerais como a maior e menor idade, e as melhores condições de veículos.
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        entregadores_unicos = df['Delivery_person_ID'].nunique()
        col1.metric('Entregadores', entregadores_unicos)
    
    with col2:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df['Distance'] = df.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        avg_distance = df['Distance'].mean()      
        col2.metric('Distância média', f"{avg_distance:.2f}")

    with col3:
        cols = ['Festival', 'Time_taken(min)']
        df_aux = df.loc[:, cols].groupby(['Festival']).mean().reset_index()
        avg_festival_time = np.round(df_aux.loc[df_aux['Festival'] == 'Yes', 'Time_taken(min)'].values[0], 2)
        col3.metric('Tempo médio de entrega com festival', avg_festival_time)

    st.write("")  # Adiciona um espaço entre as linhas de métricas

    col4, col5, col6 = st.columns(3)

    with col4:
        std_value = np.round(df.loc[df['Festival'] == 'Yes', 'Time_taken(min)'].std(), 2)
        col4.metric('Desvio padrão de entrega com festival', std_value)

    with col5:
        avg_no_festival_time = np.round(df_aux.loc[df_aux['Festival'] == 'No', 'Time_taken(min)'].values[0], 2)
        col5.metric('Tempo médio de entrega sem festival', avg_no_festival_time)

    with col6:
        std_no_festival_value = np.round(df.loc[df['Festival'] == 'No', 'Time_taken(min)'].std(), 2)
        col6.metric('Desvio padrão de entrega sem festival', std_no_festival_value)

# Função para exibir o gráfico de distribuição de tempo por cidade
def display_city_time_distribution(df):
    """
    Exibe o gráfico de tempo médio e desvio padrão por cidade.
    """
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    
    with col1:
        cols = ['City', 'Time_taken(min)']
        df_aux = df.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()

        # Criar o gráfico de barras com erros (desvio padrão)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Tempo Médio',
            x=df_aux['City'],
            y=df_aux['avg_time'],
            error_y=dict(type='data', array=df_aux['std_time']),  # Erros (desvio padrão)
            marker_color='blue'
        ))

        # Ajustar o layout do gráfico
        fig.update_layout(
            title='Tempo Médio e Desvio Padrão por Cidade',
            xaxis_title='Cidades',
            yaxis_title='Tempo (minutos)',
            barmode='group',
            width=600,
            height=500
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

    with col2:
        # Exibindo o título com tamanho de fonte 24 e negrito
        st.markdown('<h3 style="font-size: 39px; font-weight: bold;">Distribuição da Distância</h3>', unsafe_allow_html=True)
        # Seleção das colunas
        cols = ['City', 'Type_of_order', 'Time_taken(min)']
        # Realiza o agrupamento e a agregação
        df_aux = df.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
        # Resetando o índice para transformar 'Type_of_order' e 'City' em colunas
        df_aux = df_aux.reset_index()
        # Renomeando as colunas após o reset_index()
        df_aux.columns = ['Cidade', 'Tipo de Pedido', 'Média', 'Desvio Padrão']
        # Exibindo o dataframe no Streamlit
        st.dataframe(df_aux, height=450)
        
# Função para exibir os gráficos de Distância Média e Tempo/Desvio Padrão por Cidade e Tráfego
def display_avg_distance_and_time_std(df):
    """
    Exibe os gráficos de Distância Média e Tempo/Desvio Padrão por Cidade e Tráfego.
    """
    st.markdown("""---""")
    
    # Criar duas colunas lado a lado para exibir os gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distância média por cidade
        fig_avg_distance = plot_avg_distance(df)
        st.plotly_chart(fig_avg_distance, use_container_width=True)
    
    with col2:
        # Gráfico de tempo e desvio padrão por cidade e condições de tráfego
        fig_time_std = plot_time_std_by_city_traffic(df)
        st.plotly_chart(fig_time_std, use_container_width=True)

# Modificando a função principal para incluir a exibição dos gráficos
def run_dashboard(file_path):
    """
    Função principal que carrega os dados, limpa, aplica filtros e exibe o dashboard.
    """
    # Carregar e limpar os dados
    df = load_data(file_path)
    df = clean_data(df)

    # Exibir a barra lateral e aplicar filtros
    date_slider, traffic_options = sidebar()
    df_filtered = apply_filters(df, date_slider, traffic_options)

    # Exibir as diferentes componentes do dashboard
    display_overall_metrics(df_filtered)
    display_city_time_distribution(df_filtered)
    display_avg_distance_and_time_std(df_filtered)

# Rodando o app
if __name__ == '__main__':
    run_dashboard("train.csv")