import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Simulador de Importação", layout="wide")

# =========================================================
# ESTILO GLOBAL (dashboard moderno)
# =========================================================
st.markdown("""
<style>
.block-container {padding-top: 2rem;}

.card {
    padding:18px;
    border-radius:14px;
    text-align:center;
    color:white;
    font-weight:600;
    margin-bottom:10px;
}

.blue {background: linear-gradient(135deg,#2a9df4,#1d6fd8);}
.cyan {background: linear-gradient(135deg,#19c3c3,#0fa3a3);}
.green {background: linear-gradient(135deg,#17b26a,#0e8f52);}
.purple {background: linear-gradient(135deg,#6f42c1,#5a32a3);}
</style>
""", unsafe_allow_html=True)


# =========================================================
# COMPONENTES
# =========================================================
def card(titulo, valor, classe):
    st.markdown(
        f"""
        <div class="card {classe}">
            <div style="font-size:13px; opacity:.85">{titulo}</div>
            <div style="font-size:22px">R$ {valor:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def imposto(base, aliquota):
    return base * (aliquota / 100)


def grafico_donut(dados: dict, titulo: str):
    labels = []
    valores = []

    for k, v in dados.items():
        if v and v > 0:
            labels.append(k)
            valores.append(v)

    if not valores:
        st.info("Sem dados para exibir gráfico")
        return

    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=valores,
            hole=0.6,
            textinfo="percent",
            hovertemplate="%{label}<br>R$ %{value:,.2f}<extra></extra>"
        )]
    )

    fig.update_layout(
        title=titulo,
        height=320,
        margin=dict(t=40, b=0, l=0, r=0),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================================================
# ABAS
# =========================================================
tab1, tab2 = st.tabs(["🚢 Importação Mercante", "📦 Importação Simplificada"])


# =========================================================
# =================== MERCANTE ============================
# =========================================================
with tab1:

    st.title("🚢 Simulador de Importação Mercante")

    col1, col2 = st.columns(2)

    with col1:
        valor_mercadoria = st.number_input("Valor da mercadoria (R$)", min_value=0.0, step=1.0)
        frete = st.number_input("Frete internacional (R$)", min_value=0.0, step=1.0)
        seguro = st.number_input("Seguro internacional (R$)", min_value=0.0, step=1.0)

    with col2:
        armazenagem = st.number_input("Armazenagem", min_value=0.0)
        despachante = st.number_input("Despachante", min_value=0.0)
        transporte_rod = st.number_input("Transporte rodoviário", min_value=0.0)
        afrmm = st.number_input("AFRMM", min_value=0.0)

    valor_aduaneiro = valor_mercadoria + frete + seguro

    st.subheader("Alíquotas (%)")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        aliq_ii = st.number_input("II", min_value=0.0, step=0.1)
    with c2:
        aliq_ipi = st.number_input("IPI", min_value=0.0, step=0.1)
    with c3:
        aliq_pis = st.number_input("PIS", min_value=0.0, step=0.1)
    with c4:
        aliq_cofins = st.number_input("COFINS", min_value=0.0, step=0.1)
    with c5:
        aliq_icms = st.number_input("ICMS", min_value=0.0, step=0.1)

    # impostos
    ii = imposto(valor_aduaneiro, aliq_ii)
    ipi = imposto(valor_aduaneiro + ii, aliq_ipi)
    pis = imposto(valor_aduaneiro, aliq_pis)
    cofins = imposto(valor_aduaneiro, aliq_cofins)

    base_icms = valor_aduaneiro + ii + ipi + pis + cofins + afrmm
    icms = imposto(base_icms, aliq_icms)

    impostos_total = ii + ipi + pis + cofins + icms
    despesas = armazenagem + despachante + transporte_rod + afrmm
    custo_final = valor_aduaneiro + impostos_total + despesas

    st.divider()

    colr1, colr2, colr3, colr4 = st.columns(4)

    with colr1:
        card("Valor Aduaneiro", valor_aduaneiro, "blue")
    with colr2:
        card("Despesas Totais", despesas, "cyan")
    with colr3:
        card("Impostos Totais", impostos_total, "purple")
    with colr4:
        card("Custo Final", custo_final, "green")

    st.divider()

    g1, g2 = st.columns([1.2, 1])

    with g1:
        grafico_donut(
            {
                "Mercadoria": valor_mercadoria,
                "Frete/Seguro": frete + seguro,
                "Despesas": despesas,
                "Impostos": impostos_total,
            },
            "Composição do Custo"
        )

    with g2:
        grafico_donut(
            {
                "II": ii,
                "IPI": ipi,
                "PIS": pis,
                "COFINS": cofins,
                "ICMS": icms,
            },
            "Composição de Impostos"
        )


# =========================================================
# ================= SIMPLIFICADA ==========================
# =========================================================
with tab2:

    st.title("📦 Simulador de Importação Simplificada")

    col1, col2 = st.columns(2)

    with col1:
        compra = st.number_input("Valor da compra (US$)", min_value=0.0)
        dolar = st.number_input("Cotação do dólar", value=5.3, step=0.01)

    with col2:
        frete = st.number_input("Frete (R$)", min_value=0.0)
        seguro = st.number_input("Seguro (R$)", min_value=0.0)

    valor_real = compra * dolar
    vmld = valor_real + frete + seguro

    st.subheader("Alíquotas (%)")

    c1, c2, c3 = st.columns(3)

    with c1:
        aliq_ii = st.number_input("II (%)", min_value=0.0, step=0.1)
    with c2:
        aliq_icms = st.number_input("ICMS (%)", min_value=0.0, step=0.1)
    with c3:
        aliq_iof = st.number_input("IOF (%)", min_value=0.0, step=0.1)

    ii = imposto(vmld, aliq_ii)
    iof = imposto(valor_real, aliq_iof)
    icms = imposto(vmld + ii, aliq_icms)

    impostos_total = ii + icms + iof
    custo_final = vmld + impostos_total

    st.divider()

    colr1, colr2, colr3 = st.columns(3)

    with colr1:
        card("Valor em Real", valor_real, "blue")
    with colr2:
        card("Impostos", impostos_total, "purple")
    with colr3:
        card("Custo Final", custo_final, "green")

    st.divider()

    grafico_donut(
        {
            "Produto": valor_real,
            "Frete/Seguro": frete + seguro,
            "Impostos": impostos_total
        },
        "Composição do Custo"
    )
