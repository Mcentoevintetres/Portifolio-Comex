# Portfólio Comex — Algoritmos Logísticos, Aduaneiros e Regulatórios

Este repositório reúne um conjunto de algoritmos logísticos, aduaneiros e de análise estratégica de custos de comércio exterior, desenvolvidos em Python + Streamlit, com foco em simulação operacional, regulatória e apoio à decisão.

Os módulos foram projetados para reproduzir situações reais do dia a dia de operações de importação, exportação e gestão logística, transformando dados brutos em indicadores estratégicos, financeiros e regulatórios

**O objetivo do projeto é demonstrar, de forma prática e técnica, como:**
<ul>
  <li>custos logísticos impactam a operação</li>
  <li>tributos afetam a viabilidade financeira</li>
  <li>regimes especiais reduzem carga tributária</li>
  <li>algoritmos apoiam decisões operacionais</li>
</ul>

**O sistema funciona como um laboratório analítico de comércio exterior, podendo ser**

<ul>
  <li>simulações de custo</li>
  <li>estudos de viabilidade</li>
  <li>planejamento logístico</li>
  <li>análise de riscos regulatórios</li>
</ul>

# 🛰️Funcionalidades do sistema
O projeto é dividido em módulos independentes e complementares, cada um representando um problema real do setor logístico/aduaneiro.

## ✈️ Simulador de Custo de Importação Aérea
O algoritmo simula o custo total de uma operação de importação aérea, consolidando:

### Entradas:

<ul>
  <li>valor da mercadoria</li>
  <li>frete internacional</li>
  <li>seguro</li>
  <li>THC</li>
  <li>despesas logísticas adicionais</li>
  <li>impostos (II, IPI, PIS, COFINS, ICMS)</li>
</ul>

### Saidas:

<ul>
  <li>custo logístico total</li>
  <li>total de impostos</li>
  <li>custo final de importação</li>
</ul>

### Objetivo:
Avaliar viabilidade financeira da operação e identificar:

<ul>
  <li>excesso de carga tributária</li>
  <li>gargalos logísticos</li>
  <li>oportunidades de otimização</li>
</ul>

## 🚢 Simulador de Custo de Importação Marítima (Mercante + Simplificada)

Este módulo simula operações de importação marítima, contemplando dois regimes operacionais distintos:
**Importação Marítima Tradicional (Mercante)**
<ul>
  <li>cálculo completo do valor aduaneiro</li>
  <li>incidência integral de tributos</li>
  <li>aplicação de AFRMM</li>
  <li>composição detalhada do custo CIF</li>
  <li>cálculo de ICMS</li>
</ul>
**Importação Simplificada (courier / baixa complexidade)**
<ul>
  <li>estrutura tributária reduzida</li>
  <li>simplificação do fluxo de custos</li>
  <li>foco em rapidez operacional</li>
  <li>menor carga burocrática</li>
  <li>comparação direta com o modelo mercante</li>
</ul>
O objetivo é comparar custos, estrutura tributária e impacto logístico, permitindo avaliar qual modelo é mais viável dependendo do tipo de carga, valor e urgência.

## ⚖️ Módulo Regulatório — Simulador de Drawback
Ferramenta de simulação para regimes aduaneiros especiais (Drawback).

### Permite comparar:

<ul>
  <li>cenário normal (tributação integral)</li>
  <li>cenário com benefício fiscal</li>
  <li>economia tributária obtida</li>
  <li>redução percentual de custos</li>
</ul>

## 🔧 nstruções de instalação

### Clone o repositório
`git clone https://github.com/Mcentoevintetres/Portifolio-Comex.git`

### Instale as dependências
`pip install -r requirements.txt`

### Executar o sistema
`streamlit run Home.py`

## 🧪 Fundamentos técnicos aplicados

**Manipulação de dados (Pandas)**

<ul>
  <li>filtros dinâmicos</li>
  <li>agrupamentos e agregações</li>
  <li>cálculos vetorizados</li>
  <li>limpeza de dados</li>
</ul>

**Lógica e regras de negócio**

<ul>
  <li>cálculos percentuais</li>
  <li>rateio de custos</li>
  <li>composição de impostos</li>
  <li>simulação de cenários</li>
</ul>

**Estruturas condicionais**

<ul>
  <li>validação de entradas</li>
  <li>prevenção de divisão por zero</li>
  <li>tratamento de erros</li>
  <li>controle de estados no Streamlit</li>
</ul>

**Visualização**

<ul>
  <li>métricas estratégicas (st.metric)</li>
  <li>gráficos comparativos</li>
  <li>dashboards interativos</li>
</ul>

