import streamlit as st
import pandas as pd
import plotly.express as px


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Simulador de Importação Aérea",
    layout="wide"
)

# CSS
st.markdown("""
<style>
body {
    background-color: #f8fafc;
}

.kpi-card {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: white;
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    min-height: 95px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    font-family: Arial, sans-serif;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

.kpi-title {
    font-size: 13px;
    opacity: 0.85;
}

.kpi-value {
    font-size: 22px;
    font-weight: bold;
}

.section-title {
    color: #1e40af;
    font-weight: 700;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 class='section-title'>✈️ Simulador de Custo de Importação Aérea</h2>", unsafe_allow_html=True)

# FUNÇÕES AUXILIARES

def CustoRelacionados(texto):
    return st.number_input(
        texto,
        min_value=0.0,
        step=0.1,
        format="%.2f"
    )


# FUNÇÃO SEGURA PARA PERCENTUAL
def safe_percent(parte, total):
    if total <= 0:
        return 0.0
    return (parte / total) * 100

# LAYOUT PRINCIPAL

col1, col2, col3, col4 = st.columns(4)


# ---------- DADOS DA MERCADORIA ----------
with col1:
    st.markdown("### 📦 Dados da Mercadoria")

    produto = st.text_input("Produto")
    ncm = st.text_input("NCM")

    quantidade = CustoRelacionados("Quantidade")
    cubagem = CustoRelacionados("Cubagem (m³)")
    peso = CustoRelacionados("Peso bruto (Kg)")

    peso_cubado = cubagem * 167
    peso_taxavel = max(peso, peso_cubado)

    custo_unitario_usd = CustoRelacionados("Custo unitário (USD)")
    FOB = custo_unitario_usd * quantidade


# ---------- DADOS DA COTAÇÃO ----------
with col2:
    st.markdown("### ✈️ Dados da Cotação")

    frete_usd = CustoRelacionados("Frete internacional (USD)")
    seguro_percent = CustoRelacionados("Seguro (%)") / 100

    valor_seguro_usd = (FOB + frete_usd) * seguro_percent
    CIF_usd = FOB + frete_usd + valor_seguro_usd


# ---------- DESPESAS ADUANEIRAS ----------
with col3:
    st.markdown("### 🏢 Despesas Aduaneiras (BRL)")

    siscomex = CustoRelacionados("Siscomex")
    despachante = CustoRelacionados("Despachante aduaneiro")
    armazenagem = CustoRelacionados("Armazenagem aeroporto")
    awb = CustoRelacionados("Liberação AWB")
    capatazia = CustoRelacionados("Capatazia")
    taxas_aeroportuarias = CustoRelacionados("Taxas aeroportuárias")
    outras_taxas = CustoRelacionados("Outras taxas")


# ---------- CÂMBIO
with col4:
    st.markdown("### 💱 Câmbio")

    taxa_cambio = st.number_input(
        "Taxa de câmbio (BRL/USD)",
        min_value=0.01,     # evita zero
        value=5.30,        # default realista
        step=0.01,
        format="%.2f"
    )

    spread_cambial = CustoRelacionados("Spread cambial (%)") / 100
    iof_cambial = CustoRelacionados("IOF câmbio (%)") / 100

    CIF_brl = CIF_usd * taxa_cambio

# IMPOSTOS

st.markdown("---")
st.markdown("## 🧾 Impostos de Importação")

col5, col6, col7, col8, col9 = st.columns(5)

with col5:
    aliq_ii = CustoRelacionados("II (%)") / 100
with col6:
    aliq_ipi = CustoRelacionados("IPI (%)") / 100
with col7:
    aliq_pis = CustoRelacionados("PIS (%)") / 100
with col8:
    aliq_cofins = CustoRelacionados("COFINS (%)") / 100
with col9:
    aliq_icms = CustoRelacionados("ICMS (%)") / 100


II = CIF_brl * aliq_ii
IPI = (CIF_brl + II) * aliq_ipi
PIS = CIF_brl * aliq_pis
COFINS = CIF_brl * aliq_cofins


despesas_aduaneiras = (
    siscomex + despachante + armazenagem + awb +
    capatazia + taxas_aeroportuarias + outras_taxas
)

base_icms = CIF_brl + II + IPI + PIS + COFINS + despesas_aduaneiras
ICMS = (base_icms / (1 - aliq_icms)) * aliq_icms if aliq_icms > 0 else 0

impostos_totais = II + IPI + PIS + COFINS + ICMS

# CUSTOS FINAIS

custo_total = CIF_brl + impostos_totais + despesas_aduaneiras
custo_unitario_final = custo_total / quantidade if quantidade > 0 else 0

# KPIs

st.markdown("## 📊 Resumo da Importação")

k1, k2, k3, k4, k5 = st.columns(5)

def card(col, titulo, valor):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{titulo}</div>
        <div class="kpi-value">{valor}</div>
    </div>
    """, unsafe_allow_html=True)


card(k1, "FOB (USD)", f"$ {FOB:,.2f}")
card(k2, "CIF (USD)", f"$ {CIF_usd:,.2f}")
card(k3, "CIF (BRL)", f"R$ {CIF_brl:,.2f}")
card(k4, "Custo Total (BRL)", f"R$ {custo_total:,.2f}")
card(k5, "Custo Unitário (BRL)", f"R$ {custo_unitario_final:,.2f}")

# GRÁFICOS

st.markdown("## 📈 Análise dos Custos")

df_grafico = pd.DataFrame({
    "Categoria": ["CIF (BRL)", "Impostos", "Despesas Aduaneiras"],
    "Valor (BRL)": [CIF_brl, impostos_totais, despesas_aduaneiras]
})

colg1, colg2 = st.columns(2)

with colg1:
    fig_pizza = px.pie(df_grafico, names="Categoria", values="Valor (BRL)")
    st.plotly_chart(fig_pizza, use_container_width=True)

with colg2:
    fig_barra = px.bar(df_grafico, x="Categoria", y="Valor (BRL)")
    st.plotly_chart(fig_barra, use_container_width=True)

