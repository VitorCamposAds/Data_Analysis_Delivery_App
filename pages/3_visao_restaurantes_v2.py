# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime
import os
from PIL import Image
import numpy as np

st.set_page_config(page_title='Visão Restaurante', page_icon='🍽️', layout='wide')

# Leitura e limpeza dos dados
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    
    # Limpeza do dataset
    df1 = df.copy()
    
    # Remover NaN ou valores inválidos
    df1 = df1[df1['Delivery_person_Age'] != 'NaN ']
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    
    df1 = df1[df1['City'] != 'NaN ']
    df1 = df1[df1['Festival'] != 'NaN ']
    df1 = df1[df1['Road_traffic_density'] != 'NaN ']
    
    # Conversões
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    df1 = df1[df1['multiple_deliveries'] != 'NaN ']
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    # Remover espaços desnecessários nas colunas
    cols_to_strip = ['Delivery_person_ID', 'Type_of_order', 'Type_of_vehicle', 'City', 'ID', 'Road_traffic_density', 'Weatherconditions', 'Festival']
    for col in cols_to_strip:
        df1[col] = df1[col].str.strip()
    
    # Remover '(min)' da coluna 'Time_taken(min)' e converter para inteiro
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.replace(r'\(min\)', '', regex=True).astype(int)
    
    return df1

# Função para filtrar dados por data e tráfego
def filter_data(df, date_slider, traffic_options):
    # Aplicando o filtro de data
    df = df[df['Order_Date'] < date_slider]
    
    # Aplicando o filtro de tráfego
    df = df[df['Road_traffic_density'].isin(traffic_options)]
    
    return df

# Funções de métricas
def get_delivery_persons_count(df):
    return df['Delivery_person_ID'].nunique()

def get_avg_distance(df):
    cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df['Distance'] = df.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
    return df['Distance'].mean()

def get_avg_time_with_festival(df):
    df_aux = df.groupby('Festival')['Time_taken(min)'].mean().reset_index()
    return df_aux[df_aux['Festival'] == 'Yes']['Time_taken(min)'].values[0]

def get_std_time_with_festival(df):
    return np.round(df[df['Festival'] == 'Yes']['Time_taken(min)'].std(), 2)

def get_avg_time_without_festival(df):
    df_aux = df.groupby('Festival')['Time_taken(min)'].mean().reset_index()
    return df_aux[df_aux['Festival'] == 'No']['Time_taken(min)'].values[0]

def get_std_time_without_festival(df):
    return np.round(df[df['Festival'] == 'No']['Time_taken(min)'].std(), 2)

# Função para gerar o gráfico de tempo médio e desvio padrão por cidade
def plot_avg_std_by_city(df):
    df_aux = df.groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Tempo Médio',
        x=df_aux['City'],
        y=df_aux['avg_time'],
        error_y=dict(type='data', array=df_aux['std_time']),  # Erros (desvio padrão)
        marker_color='blue'
    ))

    fig.update_layout(
        title='Mean_Std por City',
        title_font=dict(size=40),
        xaxis_title='Cidades',
        yaxis_title='Tempo (minutos)',
        barmode='group',
        width=600,
        height=500
    )
    return fig

# Função para gerar o gráfico de distribuição de distância
def plot_distance_distribution(df):
    cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df['Distance'] = df.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
    avg_distance = df.groupby('City')['Distance'].mean().reset_index()

    fig = go.Figure(data=[go.Pie(labels=avg_distance["City"], values=avg_distance['Distance'], pull=[0, 0.1, 0])])
    return fig

# Função para gerar o gráfico de tempo por cidade e tipo de pedido
def plot_time_by_city_order_type(df):
    df_aux = df.groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
    df_aux.columns = ['Cidade', 'Tipo de Pedido', 'Média', 'Desvio Padrão']
    
    return df_aux

# Função para exibir o dataframe de tempos médios por cidade e tipo de pedido
def display_time_by_city_order_type(df):
    st.title('Distribuição da distância')
    cols = ['City', 'Type_of_order', 'Time_taken(min)']
    df_aux = df.groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
    df_aux.columns = ['Cidade', 'Tipo de Pedido', 'Média', 'Desvio Padrão']
    
    st.dataframe(df_aux, width=1200, height=450)

# Função principal para rodar o dashboard
def run_dashboard(file_path):
    # Carregar e limpar dados
    df = load_and_clean_data(file_path)

    # Barra lateral
    st.header('Marketplace - Visão Restaurantes')
    image_path = 'logo.jpg'
    image = Image.open(image_path)
    st.sidebar.image(image, width=220)

    st.sidebar.markdown('# Curry Company')
    st.sidebar.markdown('## Fastest Delivery in Town')
    st.sidebar.markdown("""---""")

    # Selecione uma data limite
    st.sidebar.markdown('## Selecione uma data limite')
    date_slider = st.sidebar.slider(
        'Até qual valor?',
        value=datetime(2022, 4, 13).date(),
        min_value=datetime(2022, 2, 11).date(),
        max_value=datetime(2022, 4, 6).date(),
        format='YYYY-MM-DD'
    )

    # Convertendo a data do slider para datetime64[ns]
    date_slider = pd.to_datetime(date_slider)

    # Adicionando opções para o filtro de tráfego
    st.sidebar.markdown("""---""")
    traffic_options = st.sidebar.multiselect(
        'Quais as condições do trânsito',
        ['Low', 'Medium', 'High', 'Jam'],
        default=['Low', 'Medium', 'High', 'Jam']
    )

    st.sidebar.markdown("""---""")
    st.sidebar.markdown('### @Powered by Vitor Campos Moura Costa')

    # Filtrar dados
    df = filter_data(df, date_slider, traffic_options)

    # Calcular métricas
    entregadores_unicos = get_delivery_persons_count(df)
    avg_distance = get_avg_distance(df)
    avg_festival_time = get_avg_time_with_festival(df)
    std_festival_time = get_std_time_with_festival(df)
    avg_no_festival_time = get_avg_time_without_festival(df)
    std_no_festival_time = get_std_time_without_festival(df)

    # Layout Streamlit
    st.title('Overall Metrics')

    # Exibir métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        col1.metric('Entregadores', entregadores_unicos)
    with col2:
        col2.metric(label="Distância média", value=f"{avg_distance:.2f}")
    with col3:
        col3.metric('Tempo médio de entrega com festival', f"{avg_festival_time:.2f}")

    col4, col5, col6 = st.columns(3)
    with col4:
        col4.metric('Desvio padrão de entrega com festival', f"{std_festival_time:.2f}")
    with col5:
        col5.metric('Tempo médio de entrega sem festival', f"{avg_no_festival_time:.2f}")
    with col6:
        col6.metric('Desvio padrão de entrega sem festival', f"{std_no_festival_time:.2f}")

    st.markdown("""---""")
    col1, col2 = st.columns(2)

    # Exibir gráfico de tempo médio e desvio padrão por cidade
    with col1:
        fig1 = plot_avg_std_by_city(df)
        st.plotly_chart(fig1)

    # Exibir gráfico de tempo por cidade e tipo de pedido
    with col2:
        st.markdown('<h3 style="font-size: 39px; font-weight: bold;">Distribuição da Distância</h3>', unsafe_allow_html=True)
        df_aux = plot_time_by_city_order_type(df)
        st.dataframe(df_aux, height=450)

    st.markdown("""---""")
    st.title('Distribuição do Tempo')

    col1, col2 = st.columns(2)

    with col1:
        fig2 = plot_distance_distribution(df)
        st.plotly_chart(fig2)

    with col2:
        # Gráfico de tempo médio e desvio padrão por cidade e tráfego
        cols = ['City', 'Road_traffic_density', 'Time_taken(min)']
        df_aux = df.groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)':['mean', 'std']}).reset_index()
        df_aux.columns = ['Cidade', 'Tráfego', 'Média', 'Desvio Padrão']
        
        fig3 = px.sunburst(df_aux, 
                           path=['Cidade', 'Tráfego'], 
                           values='Média', 
                           color='Desvio Padrão', 
                           color_continuous_scale='Bluered', 
                           color_continuous_midpoint=np.average(df_aux['Desvio Padrão']))
        st.plotly_chart(fig3)

    # Exibir dataframe final
    display_time_by_city_order_type(df)

# Rodar o dashboard
if __name__ == '__main__':
    run_dashboard('train.csv')
