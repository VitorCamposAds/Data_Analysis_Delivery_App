#libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime
from datetime import date
import pandas as pd 
import os
from PIL import Image

#Definindo o caminho do arquivo diretamente no código
file_path = "C:/Users/55319/Desktop/Comunidade DS/train.csv"  # Caminho fixo do arquivo

df = pd.read_csv(file_path)

#Limpeza dataset:
df1 = df.copy()

linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()
# Converter a coluna para int
df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

df1 = df1[df1['City'] != 'NaN ']
df1 = df1[df1['Festival'] != 'NaN ']
df1 = df1[df1['Road_traffic_density'] != 'NaN '] 

#2. convertendo a coluna Ratings de texto para numero decimal (float)
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

#3. convertendo a coluna order_date de texto para data
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

#4. convertendo multiple_deliveries de texto para numero inteiro (int)
linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

# 5. aplicando strip() em toda a coluna sem for:
df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Weatherconditions'] = df1.loc[:, 'Weatherconditions'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

# Remover a parte '(min)' das strings
df1['Time_taken(min)'] = df1['Time_taken(min)'].str.replace(r'\(min\)', '', regex=True)

# Converter para int
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

#===================================================
#Barra lateral
#===================================================

st.header('Marketplace - Visão Entregadores')

image_path = 'C:/Users/55319/Desktop/Comunidade DS/img/logo.jpg'
image = Image.open(image_path)
st.sidebar.image(image, width=220)

# Sidebar
st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

# Selecione uma data limite
st.sidebar.markdown('## Selecione uma data limite')

# Usando o slider no Streamlit para selecionar uma data
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13).date(),  # Data padrão
    min_value=datetime(2022, 2, 11).date(),  # Data mínima
    max_value=datetime(2022, 4, 6).date(),  # Data máxima
    format='YYYY-MM-DD'  # O formato de exibição
)

# Convertendo a data do slider para datetime64[ns] para compatibilidade
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

# Aplicando o filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]


# Aplicando o filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#===================================================
#Layout streamlit
#===================================================

def run_dashboard():
    tab1 = st.tabs(['Visão Gerencial'])[0]  # Só cria a primeira aba

    with tab1:
        with st.container():
            st.title('OVERALL METRICS')
            col1, col2, col3, col4 = st.columns(4, gap='large')
            with col1:
                #selecionando a maior idade:
                maior_idade = df1['Delivery_person_Age'].max()
                col1.metric('Maior idade', maior_idade)
                
            with col2:
                #selecionando a menor idade:
                menor_idade = df1['Delivery_person_Age'].min()
                col2.metric('Menor idade', menor_idade)
                
            with col3:
                #Selecionando a melhor condição de veículo
                melhor_condicao = df1['Vehicle_condition'].max()
                col3.metric('Melhor condição', melhor_condicao)
                
            with col4:
                #Selecionando a pior condição de veículo
                pior_condicao = df1['Vehicle_condition'].min()
                col4.metric('Pior condição', pior_condicao)
                
        with st.container():
            st.title('Avaliações')
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Média por entregador')
                colunas = ['Delivery_person_ID', 'Delivery_person_Ratings']
                media_por_entregador = df1.loc[:, colunas].groupby('Delivery_person_ID').mean().reset_index()
                st.dataframe(media_por_entregador)
                
            with col2:
                st.markdown('##### Média por trânsito')
                # Criando uma cópia do DataFrame
                df_aux = df1.copy()
                # Remover valores 'NaN' na coluna 'Road_traffic_density'
                df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
                # Selecionando as colunas de interesse
                colunas = ['Delivery_person_Ratings', 'Road_traffic_density']
                # Agrupando por 'Road_traffic_density' e calculando a média e desvio padrão das avaliações
                media_por_transito = df_aux[colunas].groupby('Road_traffic_density')['Delivery_person_Ratings'].agg(['mean', 'std']).reset_index()
                # Renomeando as colunas
                media_por_transito = media_por_transito.rename(columns={'Road_traffic_density': 'Densidade de Tráfego', 'mean': 'Média', 'std': 'Desvio Padrão'})
                # Exibindo o resultado no Streamlit
                st.dataframe(media_por_transito)
                
                st.markdown('##### Média por clima')
                df_aux = df1.copy()
                df_aux = df_aux.loc[df_aux['Weatherconditions'] != 'conditions NaN', :]
                mean_std_weather_conditions = df_aux.loc[:, ['Delivery_person_Ratings', 'Weatherconditions' ]].groupby('Weatherconditions')['Delivery_person_Ratings'].agg(['mean', 'std']).reset_index()
                mean_std_weather_conditions = mean_std_weather_conditions.rename(columns={'Weatherconditions': 'Condições Climáticas', 'mean': 'Média', 'std': 'Desvio Padrão'})
                st.dataframe(mean_std_weather_conditions)

        with st.container():
            st.markdown("""---""")
            st.title('Velocidade de Entrega')     
            col1, col2 = st.columns(2)   
            with col1:
                st.markdown('##### Mais rápidos por cidade')
                df_aux1 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)']).reset_index()
                df_aux02 = df_aux1.loc[df_aux1['City'] == 'Metropolitian', :].head(10)
                df_aux03 = df_aux1.loc[df_aux1['City'] == 'Urban', :].head(10)
                df_aux04 = df_aux1.loc[df_aux1['City'] == 'Semi-Urban', :].head(10)
                df3 = pd.concat([df_aux02, df_aux03, df_aux04]).reset_index(drop=True)
                st.dataframe(df3)
                    
            with col2:
                st.markdown('##### Mais lentos por cidade')
                df_aux1 = df_aux.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).max().sort_values(['City', 'Time_taken(min)'], ascending=False).reset_index()
                # Remover espaços em branco extras na coluna 'City'
                df_aux1['City'] = df_aux1['City'].str.strip()
                df_aux02 = df_aux1.loc[df_aux1['City'] == 'Metropolitian', :].head(10)
                df_aux03 = df_aux1.loc[df_aux1['City'] == 'Urban', :].head(10)
                df_aux04 = df_aux1.loc[df_aux1['City'] == 'Semi-Urban', :].head(10)
                df3 = pd.concat([df_aux02, df_aux03, df_aux04]).reset_index(drop=True)
                st.dataframe(df3)

# Função para rodar o app
if __name__ == '__main__':
    run_dashboard()