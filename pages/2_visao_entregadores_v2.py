# libraries
from haversine import haversine
import plotly.express as px
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image

st.set_page_config(page_title='Visão Entregadores', page_icon='🏍️', layout='wide')

# Função para carregar o dataset
def load_data(file_path):
    """
    Carrega o dataset a partir de um arquivo CSV.
    """
    return pd.read_csv(file_path)

# Função para limpar o dataset
def cleanCode(df):
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
    col1, col2, col3, col4 = st.columns(4, gap='large')
    
    with col1:
        maior_idade = df['Delivery_person_Age'].max()
        col1.metric('Maior idade', maior_idade)
    
    with col2:
        menor_idade = df['Delivery_person_Age'].min()
        col2.metric('Menor idade', menor_idade)
    
    with col3:
        melhor_condicao = df['Vehicle_condition'].max()
        col3.metric('Melhor condição', melhor_condicao)
    
    with col4:
        pior_condicao = df['Vehicle_condition'].min()
        col4.metric('Pior condição', pior_condicao)

# Função para exibir as avaliações
def display_ratings(df):
    """
    Exibe as avaliações médias por entregador, condições de trânsito e clima.
    """
    st.title('Avaliações')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('##### Média por entregador')
        media_por_entregador = df.groupby('Delivery_person_ID')['Delivery_person_Ratings'].mean().reset_index()
        st.dataframe(media_por_entregador)
    
    with col2:
        st.markdown('##### Média por trânsito')
        df_aux = df[df['Road_traffic_density'] != 'NaN']
        media_por_transito = df_aux.groupby('Road_traffic_density')['Delivery_person_Ratings'].agg(['mean', 'std']).reset_index()
        media_por_transito = media_por_transito.rename(columns={'Road_traffic_density': 'Densidade de Tráfego', 'mean': 'Média', 'std': 'Desvio Padrão'})
        st.dataframe(media_por_transito)
        
        st.markdown('##### Média por clima')
        df_aux = df[df['Weatherconditions'] != 'conditions NaN']
        mean_std_weather_conditions = df_aux.groupby('Weatherconditions')['Delivery_person_Ratings'].agg(['mean', 'std']).reset_index()
        mean_std_weather_conditions = mean_std_weather_conditions.rename(columns={'Weatherconditions': 'Condições Climáticas', 'mean': 'Média', 'std': 'Desvio Padrão'})
        st.dataframe(mean_std_weather_conditions)

# Função para exibir a velocidade de entrega
def display_delivery_speed(df):
    """
    Exibe a velocidade de entrega por cidade, tanto para os mais rápidos quanto para os mais lentos.
    """
    st.title('Velocidade de Entrega')     
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('##### Mais rápidos por cidade')
        df_aux1 = df.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)'].min().reset_index()
        df_aux1 = pd.concat([df_aux1[df_aux1['City'] == city].head(10) for city in ['Metropolitian', 'Urban', 'Semi-Urban']]).reset_index(drop=True)
        st.dataframe(df_aux1)
    
    with col2:
        st.markdown('##### Mais lentos por cidade')
        df_aux1 = df.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)'].max().reset_index()
        df_aux1 = pd.concat([df_aux1[df_aux1['City'] == city].head(10) for city in ['Metropolitian', 'Urban', 'Semi-Urban']]).reset_index(drop=True)
        st.dataframe(df_aux1)

# Função principal para rodar o dashboard
def run_dashboard(file_path):
    """
    Função principal que carrega os dados, limpa, aplica filtros e exibe o dashboard.
    """
    # Carregar e limpar os dados
    df = load_data(file_path)
    df = cleanCode(df)

    # Exibir a barra lateral e aplicar filtros
    date_slider, traffic_options = sidebar()
    df_filtered = apply_filters(df, date_slider, traffic_options)

    # Exibir os diferentes componentes do dashboard
    display_overall_metrics(df_filtered)
    display_ratings(df_filtered)
    display_delivery_speed(df_filtered)

# Rodando o app
if __name__ == '__main__':
    run_dashboard("train.csv")