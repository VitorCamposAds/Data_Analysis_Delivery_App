<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Curry Company - Análise de Marketplace</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 20px;
            text-align: center;
        }
        header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        section {
            padding: 20px;
            max-width: 1000px;
            margin: 0 auto;
            background-color: #fff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        section h2 {
            color: #2c3e50;
            font-size: 2em;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 10px;
        }
        ul {
            list-style-type: none;
            padding-left: 0;
        }
        ul li {
            margin-bottom: 10px;
        }
        .important {
            font-weight: bold;
            color: #e74c3c;
        }
        .highlight {
            color: #2980b9;
        }
        .link {
            color: #3498db;
            text-decoration: none;
        }
        .link:hover {
            text-decoration: underline;
        }
        footer {
            text-align: center;
            padding: 10px;
            background-color: #333;
            color: #fff;
        }
    </style>
</head>
<body>

<header>
    <h1>Curry Company - Análise de Marketplace</h1>
</header>

<section>
    <h2>Sobre o Projeto</h2>
    <p>
        Este projeto, ainda em andamento e em evolução, consiste em uma aplicação de análise de dados da Curry Company utilizando <strong>Streamlit</strong>, <strong>Plotly</strong>, <strong>Pandas</strong> e outras bibliotecas para explorar e visualizar dados da empresa. Através dessa aplicação, é possível ter uma visão dos dados das dimensões <em>entregadores</em>, <em>empresas</em> e <em>restaurantes</em>.
    </p>
    <p>
        <span class="important">O código ainda está em processo de modularização</span>, portanto, a versão aqui publicada trata-se de uma versão macarrônica em transição e experimentalista, embora o objetivo analítico esteja completo enquanto a versão final ainda está sendo desenvolvida.
    </p>

    <h2>Funcionalidades</h2>
    <ul>
        <li><strong>Visão Empresa</strong>: Análise geral de pedidos, tráfego e pedidos por cidade.</li>
        <li><strong>Visão Entregadores</strong>: Análise de desempenho dos entregadores, incluindo pedidos por semana e entregas por entregador.</li>
        <li><strong>Visão Geográfica</strong>: Visualização geográfica das entregas utilizando mapas interativos.</li>
    </ul>

    <h2>Tecnologias Utilizadas</h2>
    <ul>
        <li><strong>Streamlit</strong>: Framework para criação de interfaces interativas.</li>
        <li><strong>Plotly</strong>: Biblioteca para visualizações gráficas interativas.</li>
        <li><strong>Pandas</strong>: Manipulação e análise de dados.</li>
        <li><strong>Folium</strong>: Criação de mapas interativos.</li>
        <li><strong>Haversine</strong>: Cálculo de distâncias geográficas.</li>
        <li><strong>Pillow</strong>: Manipulação de imagens.</li>
    </ul>

    <h2>Pré-requisitos</h2>
    <p>
        Certifique-se de ter o <strong>Python 3.x</strong> instalado no seu ambiente.
    </p>
    <p>
        As dependências do projeto estão listadas no arquivo <code>requirements.txt</code>.
    </p>

    <h2>Acesso aos Dashboards</h2>
    <p>
        Você pode acessar os dashboards hospedados no Streamlit Cloud através do link: 
        <a href="https://dataanalysisdeliveryapp-pwdtvg6r8z5cskxmk6jzsw.streamlit.app/" class="link" target="_blank">
            Dashboard Curry Company
        </a>.
    </p>
</section>

<footer>
    <p>&copy; 2024 Curry Company (Vitor Campos) - Todos os direitos reservados.</p>
</footer>

</body>
</html>

