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

#Definindo o caminho do arquivo diretamente no código
file_path = "C:/Users/55319/Desktop/Comunidade DS/train.csv"  # Caminho fixo do arquivo

df = pd.read_csv(file_path)

def run_dashboard():
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

    st.header('Marketplace - Visão Restaurantes')

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

    tab1 = st.tabs(['Visão Restaurantes'])[0]  # Só cria a primeira aba
    with tab1:
        with st.container():
            st.title('Overall Metrics')

        col1, col2, col3 = st.columns(3)
        
        with col1:
            entregadores_unicos = df1['Delivery_person_ID'].nunique()
            col1.metric('Entregadores', entregadores_unicos)

        with col2:
            cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            df1['Distance'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
            avg_distance = df1['Distance'].mean()      
            col2.metric(label="Distância média", value=f"{avg_distance:.2f}")

        with col3:
            cols = ['Festival', 'Time_taken(min)']
            df_aux = df1.loc[:, cols].groupby(['Festival']).mean().reset_index()
            avg_festival_time = np.round(df_aux.loc[df_aux['Festival'] == 'Yes', 'Time_taken(min)'].values[0], 2)
            col3.metric('Tempo médio de entrega com festival', avg_festival_time)

        st.write("")  # Adiciona um espaço entre as linhas de métricas

        col4, col5, col6 = st.columns(3)

        with col4:
            std_value = np.round(df1.loc[df1['Festival'] == 'Yes', 'Time_taken(min)'].std(), 2)
            col4.metric('Desvio padrão de entrega com festival', std_value)

        with col5:
            avg_no_festival_time = np.round(df_aux.loc[df_aux['Festival'] == 'No', 'Time_taken(min)'].values[0], 2)
            col5.metric('Tempo médio de entrega sem festival', avg_no_festival_time)

        with col6:
            std_no_festival_value = np.round(df1.loc[df1['Festival'] == 'No', 'Time_taken(min)'].std(), 2)
            col6.metric('Desvio padrão de entrega sem festival', std_no_festival_value)
    ###      
        with st.container():
            st.markdown("""---""")
            col1, col2 = st.columns(2)
            with col1:
                cols = ['City', 'Time_taken(min)']
                df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
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
                    title='Time (mean/std) by City',
                    title_font=dict(size=42),
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
                df_aux = df1.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
                # Resetando o índice para transformar 'Type_of_order' e 'City' em colunas
                df_aux = df_aux.reset_index()
                # Renomeando as colunas após o reset_index()
                df_aux.columns = ['Cidade', 'Tipo de Pedido', 'Média', 'Desvio Padrão']
                # Exibindo o dataframe no Streamlit
                st.dataframe(df_aux, height=450)
            
        with st.container():
            st.markdown("""---""")
            st.title('Distribuição do tempo')
            col1, col2 = st.columns(2)
                
            # Gráfico 1 - Distância média
            with col1:
                cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
                df1['Distance'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
                avg_distance = df1.loc[:, ['City', 'Distance']].groupby('City').mean().reset_index()
                
                # Plotar o gráfico de pizza
                fig = go.Figure(data=[go.Pie(labels=avg_distance["City"], values=avg_distance['Distance'], pull=[0, 0.1, 0])])
                st.plotly_chart(fig)

        # Gráfico 2 - Tempo médio e desvio padrão por cidade e tráfego
            with col2:
                cols = ['City', 'Road_traffic_density', 'Time_taken(min)']
                df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)':['mean', 'std']})
                df_aux = df_aux.reset_index()

                # Renomear as colunas para torná-las mais amigáveis
                df_aux.columns = ['Cidade', 'Tráfego', 'Média', 'Desvio Padrão']

                # Plotar o gráfico sunburst
                fig = px.sunburst(df_aux, 
                                path=['Cidade', 'Tráfego'], 
                                values='Média', 
                                color='Desvio Padrão', 
                                color_continuous_scale='Bluered', 
                                color_continuous_midpoint=np.average(df_aux['Desvio Padrão']))
                
                # Exibir o gráfico
                st.plotly_chart(fig)
                        
        with st.container():
            st.markdown("""---""")
            st.title('Distribuição da distância')
            # Seleção das colunas
            cols = ['City', 'Type_of_order', 'Time_taken(min)']

            # Realiza o agrupamento e a agregação
            df_aux = df1.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})

            # Resetando o índice para transformar 'Type_of_order' e 'City' em colunas
            df_aux = df_aux.reset_index()

            # Renomeando as colunas após o reset_index()
            df_aux.columns = ['Cidade', 'Tipo de Pedido', 'Média', 'Desvio Padrão']

            # Exibindo o dataframe no Streamlit
            st.dataframe(df_aux, width=1200, height=450)

# Função para rodar o app
if __name__ == '__main__':
    run_dashboard()