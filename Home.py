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
st.sidebar.markdown('<h1 style="color: #4CAF50;">Curry Company</h1>', unsafe_allow_html=True)
st.sidebar.markdown('<h2 style="color: #555;">Fastest Delivery in Town</h2>', unsafe_allow_html=True)
st.sidebar.markdown("""<hr style="border: 1px solid #4CAF50;">""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 style="color: #4CAF50;">Curry Company Growth Dashboard</h1>', unsafe_allow_html=True)

# Conteúdo do dashboard
st.markdown(
    """
    <div style="font-size: 18px; color: #333;">
        Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
        <h3>Como utilizá-lo?</h3>
        <ul>
            <li><strong>Visão Empresa:</strong>
                <ul>
                    <li>Visão Gerencial: Métricas gerais de comportamento.</li>
                    <li>Visão Tática: Indicadores semanais de crescimento.</li>
                    <li>Visão Geográfica: Insights de geolocalização.</li>
                </ul>
            </li>
            <li><strong>Visão Entregador:</strong>
                <ul>
                    <li>Acompanhamento dos indicadores semanais de crescimento.</li>
                </ul>
            </li>
            <li><strong>Visão Restaurante:</strong>
                <ul>
                    <li>Indicadores semanais de crescimento dos restaurantes.</li>
                </ul>
            </li>
        </ul>
        <h3>Ask for Help</h3>
        <p><a href="mailto:vitorbeatle@gmail.com">vitorbeatle@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True
)