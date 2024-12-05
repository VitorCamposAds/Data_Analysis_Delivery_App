import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🎲"
)

# Carregar a imagem
image_path = 'logo.jpg'
image = Image.open(image_path)
st.sidebar.image(image, width=220)

# Sidebar
st.sidebar.markdown("# Curry Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("---")

# Título principal
st.markdown("# Curry Company Growth Dashboard")

# Conteúdo do dashboard
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    
    ### Como utilizá-lo?
    - **Visão Empresa:**
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - **Visão Entregador:**
        - Acompanhamento dos indicadores semanais de crescimento.
    - **Visão Restaurante:**
        - Indicadores semanais de crescimento dos restaurantes.
    
    ### Ask for Help
    vitorbeatle@gmail.com
    """
)