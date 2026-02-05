import streamlit as st

st.set_page_config(
    page_title="Portfólio Comex",
    layout="wide"
)

# OCULTAR SIDEBAR
st.markdown("""
<style>
section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# CSS (somente visual)
st.markdown("""
<style>

.card {
    padding: 22px;
    border-radius: 14px;
    background-color: #E7F0FF !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.18);
    border: 1px solid #3B82F6;
    transition: 0.2s;
    cursor: pointer;
    height: 150px;
}

.card:hover {
    transform: translateY(-4px);
    background-color: white !important;
}

.card-title {
    font-size: 18px;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 6px;
}

.card-desc {
    font-size: 14px;
    color: #374151;
}

a {
    text-decoration: none !important;
}

</style>
""", unsafe_allow_html=True)

# HEADER

st.title("🌎 Portfólio de Algoritmos de Comércio Exterior")

st.info(
    "Simuladores financeiros, tributários e operacionais para processos de Importação, "
    "Drawback e cálculo de custos logísticos internacionais."
)

st.caption("Todos os valores utilizados são demonstrativos.")

# COMPONENTE CARD

def card(title, desc, page):
    st.markdown(f"""
    <a href="/{page}" target="_self">
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="large")

with col1:
    card(
        "📑 Drawback",
        "Simulador regulatório • suspensão • isenção • cálculo de tributos.",
        "drawback"
    )

with col2:
    card(
        "✈️ Importação Aérea",
        "Custos CIF • impostos • VMLE • despesas aeroportuárias.",
        "Importacao_aerea"
    )

with col3:
    card(
        "🚢 Importação Mercante",
        "Frete marítimo • AFRMM • ICMS • armazenagem • despesas portuárias.",
        "importacao_mercante"
    )

with col4:
    card(
        "📦 Importação Simplificada",
        "Remessa expressa • DSI • II • ICMS • IOF • taxas operacionais.",
        "importacao_mercante"
    )
