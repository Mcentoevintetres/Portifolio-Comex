import streamlit as st
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Drawback Regulatório", layout="wide")

# ======================================================
# ESTILO
# ======================================================
st.markdown("""
<style>
.card {
    padding:18px;
    border-radius:14px;
    text-align:center;
    color:white;
    font-weight:600;
    margin-bottom:10px;
}
.blue {background: linear-gradient(135deg,#2a9df4,#1d6fd8);}
.green {background: linear-gradient(135deg,#17b26a,#0e8f52);}
.orange {background: linear-gradient(135deg,#ff9800,#ef6c00);}
.red {background: linear-gradient(135deg,#f44336,#c62828);}
.purple {background: linear-gradient(135deg,#6f42c1,#5a32a3);}
</style>
""", unsafe_allow_html=True)

# ======================================================
# COMPONENTES
# ======================================================
def card(titulo, valor, classe):
    st.markdown(
        f"""
        <div class="card {classe}">
            <div style="font-size:13px; opacity:.85">{titulo}</div>
            <div style="font-size:22px">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def imposto(base, aliquota):
    return base * (aliquota / 100)

def grafico_donut(dados, titulo):
    labels, valores = [], []
    for k, v in dados.items():
        if v > 0:
            labels.append(k)
            valores.append(v)

    if not valores:
        st.info("Sem dados para gráfico")
        return

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.6,
        hovertemplate="%{label}<br>R$ %{value:,.2f}<extra></extra>"
    )])

    fig.update_layout(
        title=titulo,
        height=320,
        margin=dict(t=40, b=0, l=0, r=0)
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# REGRAS DRAWBACK
# ======================================================
REGRAS_DRAWBACK = {
    "Suspensão": ["II", "IPI", "PIS", "COFINS"],
    "Isenção": ["II", "IPI", "PIS", "COFINS"],
    "Restituição": ["II", "IPI"]
}

# ======================================================
# DASHBOARD
# ======================================================
st.title("📑 Módulo Regulatório Drawback")

# ---------------- CONFIGURAÇÃO DO ATO ------------------
st.subheader("Configuração do Ato Concessório")

c1, c2, c3 = st.columns(3)

with c1:
    numero_ato = st.text_input("Número do Ato")
    modalidade = st.selectbox("Modalidade", list(REGRAS_DRAWBACK.keys()))
    ncm = st.text_input("NCM")

with c2:
    data_inicio = st.date_input("Data início", date.today())
    data_fim = st.date_input("Data fim")
    produto_final = st.text_input("Produto final")

with c3:
    coeficiente = st.number_input("Coeficiente técnico", min_value=0.0, step=0.01)
    qtd_autorizada = st.number_input("Qtd autorizada", min_value=0.0)
    valor_autorizado = st.number_input("Valor autorizado (R$)", min_value=0.0)

# ---------------- MOVIMENTAÇÃO -------------------------
st.subheader("Movimentação")

m1, m2, m3 = st.columns(3)

with m1:
    importado_qtd = st.number_input("Qtd importada", min_value=0.0)
    importado_valor = st.number_input("Valor importado (R$)", min_value=0.0)

with m2:
    exportado_qtd = st.number_input("Qtd exportada", min_value=0.0)

with m3:
    dias_restantes = (data_fim - date.today()).days
    status = "🟢 Regular" if dias_restantes > 60 else "🟠 Atenção" if dias_restantes > 0 else "🔴 Vencido"

# ---------------- SALDOS -------------------------------
saldo_qtd = qtd_autorizada - importado_qtd
cumprimento = (exportado_qtd / importado_qtd * 100) if importado_qtd > 0 else 0

# ---------------- IMPOSTOS -----------------------------
st.subheader("Alíquotas (%)")

i1, i2, i3, i4, i5 = st.columns(5)

with i1: aliq_ii = st.number_input("II", 0.0)
with i2: aliq_ipi = st.number_input("IPI", 0.0)
with i3: aliq_pis = st.number_input("PIS", 0.0)
with i4: aliq_cofins = st.number_input("COFINS", 0.0)
with i5: aliq_icms = st.number_input("ICMS", 0.0)

# impostos potenciais
ii = imposto(importado_valor, aliq_ii)
ipi = imposto(importado_valor + ii, aliq_ipi)
pis = imposto(importado_valor, aliq_pis)
cofins = imposto(importado_valor, aliq_cofins)
icms = imposto(importado_valor, aliq_icms)

# economia
economia = 0
for tributo in REGRAS_DRAWBACK[modalidade]:
    economia += locals()[tributo.lower()]

# ---------------- DASHBOARD ----------------------------
st.divider()

d1, d2, d3, d4 = st.columns(4)

with d1:
    card("Status do Ato", status, "blue")
with d2:
    card("Dias Restantes", f"{dias_restantes} dias", "purple")
with d3:
    card("Cumprimento", f"{cumprimento:.1f} %", "green")
with d4:
    card("Economia Realizada", f"R$ {economia:,.2f}", "orange")

st.divider()

g1, g2 = st.columns(2)

with g1:
    grafico_donut(
        {
            "II": ii,
            "IPI": ipi,
            "PIS": pis,
            "COFINS": cofins,
            "ICMS": icms
        },
        "Tributos Envolvidos"
    )

with g2:
    grafico_donut(
        {
            "Economia com Drawback": economia,
            "Tributos Não Beneficiados": icms
        },
        "Impacto Financeiro"
    )
