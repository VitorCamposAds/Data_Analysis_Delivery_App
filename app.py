import streamlit as st
import importlib
# Configuração da página do Streamlit
st.set_page_config(layout="wide")

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
