# README

## 1. Problema de negócio
A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas. Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por um entregador também cadastrado no aplicativo da Cury Company.

A empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos entregadores, etc. Apesar da entrega estar crescendo, em termos de entregas, o CEO não tem visibilidade completa dos KPIs de crescimento da empresa.

A Cury Company possui um modelo de negócio chamado Marketplace, que faz o intermédio do negócio entre três clientes principais: Restaurantes, entregadores e pessoas compradoras. Para acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento:

### Do lado da empresa:
1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por cidade e tipo de tráfego.
5. A quantidade de pedidos por entregador por semana.
6. A localização central de cada cidade por tipo de tráfego.

### Do lado do entregador:
1. A menor e maior idade dos entregadores.
2. A pior e a melhor condição de veículos.
3. A avaliação média por entregador.
4. A avaliação média e o desvio padrão por tipo de tráfego.
5. A avaliação média e o desvio padrão por condições climáticas.
6. Os 10 entregadores mais rápidos por cidade.
7. Os 10 entregadores mais lentos por cidade.

### Do lado do restaurante:
1. A quantidade de entregadores únicos.
2. A distância média dos restaurantes e dos locais de entrega.
3. O tempo médio e o desvio padrão de entrega por cidade.
4. O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
5. O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
6. O tempo médio de entrega durante os festivais.

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

---

## 2. Premissas assumidas para a análise
1. A análise foi realizada com dados entre 11/02/2022 e 06/04/2022.
2. Marketplace foi o modelo de negócio assumido.
3. Os 3 principais focos do negócio foram: Visão de transação de pedidos, visão de restaurantes e visão de entregadores.

---

## 3. Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa:

### 1. Visão do crescimento da empresa
- Pedidos por dia
- Porcentagem de pedidos por condições de trânsito
- Quantidade de pedidos por tipo e por cidade
- Pedidos por semana
- Quantidade de pedidos por tipo de entrega
- Quantidade de pedidos por condições de trânsito e tipo de cidade

### 2. Visão do crescimento dos restaurantes
- Quantidade de pedidos únicos.
- Distância média percorrida.
- Tempo médio de entrega durante festivais e dias normais.
- Desvio padrão do tempo de entrega durante festivais e dias normais.
- Tempo de entrega médio por cidade.
- Distribuição do tempo médio de entrega por cidade.
- Tempo médio de entrega por tipo de pedido.

### 3. Visão do crescimento dos entregadores
- Idade do entregador mais velho e do mais novo.
- Avaliação do melhor e do pior veículo.
- Avaliação média por entregador.
- Avaliação média por condições de trânsito.
- Avaliação média por condições climáticas.
- Tempo médio do entregador mais rápido.
- Tempo médio do entregador mais rápido por cidade.

---

## 4. Top 3 Insights de dados
1. A sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em dias sequenciais.
2. As cidades do tipo Semi-Urban não possuem condições baixas de trânsito.
3. As maiores variações no tempo de entrega acontecem durante o clima ensolarado.

---

## 5. O produto final do projeto
O produto final do projeto é um painel online, hospedado na nuvem e disponível para acesso em qualquer dispositivo conectado à internet. O painel pode ser acessado através do seguinte link:

[Dashboard Curry Company 1](https://vitorcampos-curry-company.streamlit.app/)

---

## 6. Conclusão
O objetivo desse projeto foi criar um conjunto de gráficos e/ou tabelas que exibem as métricas da melhor forma possível para o CEO. Da visão da empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e a semana 13 do ano de 2022.

---

## 7. Próximos passos
1. Reduzir o número de métricas.
2. Criar novos filtros.
3. Adicionar novas visões de negócio.
