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


def run_dashboard():
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

#===================================================
# Layout Streamlit
#===================================================

    tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Estratégica', 'Visão Geográfica'])

    with tab1:
        # Pedidos Diários
        with st.container():
            st.markdown('# Pedidos Diários')
            cols = ['ID', 'Order_Date']
            selecao = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
            fig = px.bar(selecao, x='Order_Date', y='ID')
            st.plotly_chart(fig, use_container_width=True)

        # Pedidos X Tráfego e Pedidos por Cidade e Tráfego
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('### Pedidos X Tráfego')
                df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
                df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum() * 100
                fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown('### Pedidos por Cidade e Tráfego')
                df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
                df_aux = df_aux[df_aux['City'] != 'NaN']
                df_aux = df_aux[df_aux['Road_traffic_density'] != 'NaN']
                fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Pedidos por Semana
        with st.container():
            st.markdown("# Pedidos por Semana")
            df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U')
            qtd_semana = df1.loc[:, ['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index()
            fig = px.line(qtd_semana, x='Week_of_year', y='ID')
            st.plotly_chart(fig, use_container_width=True)

        # Pedidos por Semana por Entregador
        with st.container():
            df_aux1 = df1.loc[:, ['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index()
            df_aux2 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby('Week_of_year')['Delivery_person_ID'].nunique().reset_index()
            df_aux = pd.merge(df_aux1, df_aux2, how='inner')
            df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
            fig = px.line(df_aux, x='Week_of_year', y='order_by_deliver')
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Localização por Tráfego
        st.markdown("# Localização por Tráfego")
        df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]\
            .groupby(['City', 'Road_traffic_density']).median().reset_index()

        df_aux = df_aux[df_aux['City'] != 'NaN']
        df_aux = df_aux[df_aux['Road_traffic_density'] != 'NaN']

        map = folium.Map()
        for index, location_info in df_aux.iterrows():
            folium.Marker(
                [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']],
                popup=f"City: {location_info['City']}<br>Traffic: {location_info['Road_traffic_density']}"
            ).add_to(map)

        folium_static(map, width=700, height=350)

# Função para rodar o app
if __name__ == '__main__':
    run_dashboard()