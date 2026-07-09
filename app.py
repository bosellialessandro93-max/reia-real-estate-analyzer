import streamlit as st
import pandas as pd
import plotly.express as px

from utils.calculations import calculate_investment, euro, pct

st.set_page_config(
    page_title="REIA PRO - Via Capuana 58",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}
.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    margin-bottom: 18px;
}
.big-title {
    font-size: 42px;
    font-weight: 800;
}
.subtitle {
    font-size: 18px;
    color: #6b7280;
}
.score {
    font-size: 58px;
    font-weight: 900;
    color: #0a7f45;
}
.small-note {
    color: #6b7280;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DEFAULT DATA - VIA CAPUANA 58
# -----------------------------
default_data = {
    "prezzo_acquisto": 70000,
    "mq": 75,
    "ristrutturazione": 10000,
    "arredo": 7000,
    "spese_acquisto": 6000,
    "anticipo_pct": 10,
    "tasso": 3.0,
    "durata_anni": 25,
    "occupazione": 48,
    "adr": 105,
    "costi_operativi_pct": 35,
    "tassazione_pct": 21,
    "valore_rivendita_mq": 1800,
    "anni_exit": 5,
    "crescita_annua": 3.0,
    "posizione_score": 72,
    "rischio_score": 75,
    "airbnb_score": 79,
    "stato_score": 82,
}

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🏠 REIA PRO")
st.sidebar.caption("Caso studio: Rho - Via Capuana 58")

page = st.sidebar.radio(
    "Navigazione",
    [
        "Executive Dashboard",
        "Analisi di Mercato",
        "Scheda Immobile",
        "Business Plan",
        "Airbnb",
        "Rivendita",
        "REIA Score",
        "Due Diligence",
        "Verdetto"
    ]
)

st.sidebar.divider()
st.sidebar.header("Parametri modificabili")

data = default_data.copy()

data["prezzo_acquisto"] = st.sidebar.number_input("Prezzo acquisto (€)", value=data["prezzo_acquisto"], step=1000)
data["ristrutturazione"] = st.sidebar.number_input("Ristrutturazione (€)", value=data["ristrutturazione"], step=1000)
data["arredo"] = st.sidebar.number_input("Arredo (€)", value=data["arredo"], step=1000)
data["spese_acquisto"] = st.sidebar.number_input("Spese acquisto (€)", value=data["spese_acquisto"], step=500)

data["occupazione"] = st.sidebar.slider("Occupazione Airbnb (%)", 10, 90, data["occupazione"])
data["adr"] = st.sidebar.number_input("ADR medio (€)", value=data["adr"], step=5)

data["anticipo_pct"] = st.sidebar.slider("Anticipo mutuo (%)", 0, 100, data["anticipo_pct"])
data["tasso"] = st.sidebar.slider("Tasso mutuo (%)", 1.0, 7.0, data["tasso"], 0.1)
data["durata_anni"] = st.sidebar.slider("Durata mutuo", 5, 30, data["durata_anni"])

data["valore_rivendita_mq"] = st.sidebar.number_input("Valore rivendita €/mq", value=data["valore_rivendita_mq"], step=50)
data["crescita_annua"] = st.sidebar.slider("Crescita annua valore (%)", -5.0, 8.0, data["crescita_annua"], 0.5)

result = calculate_investment(data)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="big-title">🏠 REIA PRO</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Real Estate Investment Analyzer - Caso studio: trilocale Airbnb / rivendita - Via Luigi Capuana 58, Rho</div>',
    unsafe_allow_html=True
)
st.divider()

# -----------------------------
# EXECUTIVE DASHBOARD
# -----------------------------
if page == "Executive Dashboard":

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("REIA Score", f"{result['reia_score']}/100")
    col2.metric("Investimento totale", euro(result["investimento_totale"]))
    col3.metric("Cash Flow netto annuo", euro(result["cash_flow_netto"]))
    col4.metric("Capital Gain stimato", euro(result["capital_gain"]))

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Costo reale €/mq", f"{result['costo_mq']:,.0f} €/mq".replace(",", "."))
    col6.metric("Rata mutuo mensile", euro(result["rata_mensile"]))
    col7.metric("Ricavi lordi Airbnb", euro(result["ricavi_lordi"]))
    col8.metric("Valore futuro stimato", euro(result["valore_futuro"]))

    st.divider()

    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.subheader("📈 Proiezione valore immobile")
        anni = list(range(0, data["anni_exit"] + 1))
        valori = [
            result["valore_attuale"] * ((1 + data["crescita_annua"] / 100) ** i)
            for i in anni
        ]
        df = pd.DataFrame({"Anno": anni, "Valore stimato": valori})
        fig = px.line(df, x="Anno", y="Valore stimato", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("🧠 Sintesi AI")
        st.success(f"Verdetto provvisorio: {result['verdict']}")
        st.write(
            """
            L'investimento appare interessante soprattutto per il prezzo di ingresso molto basso
            rispetto ai valori medi della zona. Airbnb rappresenta la strategia di copertura del mutuo,
            mentre la parte più rilevante del rendimento atteso deriva dalla rivalutazione e dalla rivendita.
            """
        )

# -----------------------------
# ANALISI DI MERCATO
# -----------------------------
elif page == "Analisi di Mercato":

    st.header("📊 Analisi di Mercato - Via Capuana 58, Rho")

    st.subheader("1. Posizionamento dell'immobile")
    st.write("""
    L'immobile si trova in Via Luigi Capuana 58, Rho. La posizione non è premium come centro Rho o zona stazione,
    ma è funzionale per una strategia Airbnb orientata a Fiera Milano Rho, Molino Dorino, lavoratori, tecnici,
    espositori e famiglie.
    """)

    market = pd.DataFrame({
        "Elemento": [
            "Comune",
            "Microzona",
            "Target principale",
            "Target secondario",
            "Strategia",
            "Punto di forza",
            "Punto debole"
        ],
        "Valutazione": [
            "Rho, area metropolitana Milano",
            "Residenziale funzionale, non turistica pura",
            "Fiera Milano / business / tecnici",
            "Famiglie e soggiorni low-cost verso Milano",
            "Airbnb primi anni + rivendita con plusvalenza",
            "Prezzo di acquisto molto sotto mercato",
            "Piano terra e assenza balcone"
        ]
    })
    st.dataframe(market, use_container_width=True, hide_index=True)

    st.subheader("2. Stima valore immobiliare")
    values = pd.DataFrame({
        "Scenario": ["Prudente", "Realistico", "Ottimistico"],
        "€/mq stimato": [1625, 1800, 1975],
        "Valore immobile": [1625 * 75, 1800 * 75, 1975 * 75]
    })
    st.dataframe(values, use_container_width=True, hide_index=True)

    fig = px.bar(values, x="Scenario", y="Valore immobile", text="Valore immobile")
    fig.update_traces(texttemplate="%{text:,.0f} €", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("3. Domanda potenziale")
    domanda = pd.DataFrame({
        "Segmento": [
            "Espositori Fiera Milano",
            "Tecnici e squadre di lavoro",
            "Famiglie",
            "Visitatori Milano low-cost",
            "Trasferte aziendali"
        ],
        "Forza domanda": [9, 8, 7, 6, 8],
        "Valore economico": [9, 8, 7, 6, 8]
    })
    st.dataframe(domanda, use_container_width=True, hide_index=True)

    fig2 = px.bar(domanda, x="Segmento", y=["Forza domanda", "Valore economico"], barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("4. Lettura strategica")
    st.info("""
    Il progetto non deve essere letto come semplice investimento Airbnb. La tesi di investimento è:
    acquistare sotto mercato, valorizzare con ristrutturazione mirata, generare cassa tramite affitti brevi
    e rivendere entro 5 anni con una possibile plusvalenza.
    """)

# -----------------------------
# SCHEDA IMMOBILE
# -----------------------------
elif page == "Scheda Immobile":

    st.header("🏘️ Scheda tecnica immobile")

    scheda = pd.DataFrame({
        "Caratteristica": [
            "Indirizzo",
            "Tipologia",
            "Superficie",
            "Locali",
            "Camere",
            "Bagni",
            "Cucina",
            "Piano",
            "Balcone",
            "Cantina",
            "Parcheggio",
            "Ascensore",
            "Barriere architettoniche",
            "Impianti",
            "Ristrutturazione prevista",
            "Arredo",
            "Strategia"
        ],
        "Dato": [
            "Via Luigi Capuana 58, Rho",
            "Trilocale",
            "75 mq",
            "3",
            "2",
            "1",
            "Open space con sala",
            "Piano terra",
            "No",
            "Sì, compresa nel prezzo",
            "Esterno",
            "Sì, accesso al -1",
            "Assenti / presenti scivoli e piattaforme",
            "Da non rifare",
            "Bagno + finiture leggere",
            "Completo per Airbnb",
            "Affitto breve iniziale + rivendita"
        ]
    })

    st.dataframe(scheda, use_container_width=True, hide_index=True)

    st.subheader("Valutazione qualitativa")
    col1, col2, col3 = st.columns(3)
    col1.metric("Funzionalità Airbnb", "8/10")
    col2.metric("Rivendibilità", "7,5/10")
    col3.metric("Potenziale Value Add", "9/10")

    st.write("""
    Il trilocale ha una buona struttura per ospitare 4-6 persone. Il piano terra e l'assenza del balcone sono limiti,
    ma vengono parzialmente compensati dall'accessibilità, dalla presenza della cantina, dalle finestre in ogni stanza
    e dal fatto che gli impianti non richiedono rifacimento completo.
    """)

# -----------------------------
# BUSINESS PLAN
# -----------------------------
elif page == "Business Plan":

    st.header("💰 Business Plan")

    bp = pd.DataFrame({
        "Voce": [
            "Prezzo acquisto",
            "Ristrutturazione",
            "Arredo",
            "Spese acquisto",
            "Investimento totale",
            "Ricavi lordi Airbnb",
            "Costi operativi",
            "NOI",
            "Tasse stimate",
            "Rata mutuo annua",
            "Cash Flow netto"
        ],
        "Importo": [
            data["prezzo_acquisto"],
            data["ristrutturazione"],
            data["arredo"],
            data["spese_acquisto"],
            result["investimento_totale"],
            result["ricavi_lordi"],
            result["costi_operativi"],
            result["noi"],
            result["tasse"],
            result["rata_annua"],
            result["cash_flow_netto"]
        ]
    })

    st.dataframe(bp, use_container_width=True, hide_index=True)

    fig = px.bar(bp, x="Voce", y="Importo")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# AIRBNB
# -----------------------------
elif page == "Airbnb":

    st.header("🏡 Analisi Airbnb")

    scenari = pd.DataFrame({
        "Scenario": ["Prudente", "Realistico", "Ottimizzato", "Forte/Eventi"],
        "Occupazione": [35, 48, 55, 60],
        "ADR": [85, 105, 125, 140]
    })

    scenari["Notti annue"] = scenari["Occupazione"] / 100 * 365
    scenari["Ricavi lordi"] = scenari["Notti annue"] * scenari["ADR"]

    st.dataframe(scenari, use_container_width=True, hide_index=True)

    fig = px.bar(scenari, x="Scenario", y="Ricavi lordi", text="Ricavi lordi")
    fig.update_traces(texttemplate="%{text:,.0f} €", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    La strategia consigliata è pricing dinamico: prezzo competitivo nei periodi normali,
    incremento aggressivo durante Fiera Milano, eventi business e settimane ad alta domanda.
    """)

# -----------------------------
# RIVENDITA
# -----------------------------
elif page == "Rivendita":

    st.header("📈 Exit Strategy")

    col1, col2, col3 = st.columns(3)
    col1.metric("Valore attuale stimato", euro(result["valore_attuale"]))
    col2.metric("Valore futuro stimato", euro(result["valore_futuro"]))
    col3.metric("Capital Gain lordo", euro(result["capital_gain"]))

    st.write("""
    La strategia suggerita è mantenere l'immobile per circa 5 anni, generando cassa con Airbnb
    e poi valutando la rivendita se il mercato conferma una plusvalenza significativa.
    """)

# -----------------------------
# REIA SCORE
# -----------------------------
elif page == "REIA Score":

    st.header("⭐ REIA Score")
    st.markdown(f'<div class="score">{result["reia_score"]}/100</div>', unsafe_allow_html=True)
    st.success(result["verdict"])

    score_df = pd.DataFrame({
        "Area": list(result["score_details"].keys()),
        "Score": list(result["score_details"].values())
    })

    fig = px.bar(score_df, x="Area", y="Score")
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(score_df, use_container_width=True, hide_index=True)

# -----------------------------
# DUE DILIGENCE
# -----------------------------
elif page == "Due Diligence":

    st.header("📋 Due Diligence")

    checks = [
        "Conformità catastale",
        "Conformità urbanistica",
        "APE",
        "Verifica umidità piano terra",
        "Stato serramenti",
        "Verbali condominiali ultimi 5 anni",
        "Lavori straordinari deliberati",
        "Regolamento condominiale",
        "Spese condominiali annue",
        "Verifica possibilità affitti brevi",
        "Preventivo bagno definitivo",
        "Verifica fibra internet",
        "Verifica imposte acquisto",
        "Simulazione mutuo reale"
    ]

    for c in checks:
        st.checkbox(c)

    st.warning("Prima del rogito la due diligence deve essere completata con documenti reali.")

# -----------------------------
# VERDETTO
# -----------------------------
elif page == "Verdetto":

    st.header("✅ Verdetto provvisorio")

    st.success(f"Raccomandazione: {result['verdict']}")

    st.write(f"""
    L'immobile di Via Capuana 58 presenta un investimento totale stimato di **{euro(result['investimento_totale'])}**,
    con un costo reale pari a circa **{result['costo_mq']:,.0f} €/mq**.
    """.replace(",", "."))

    st.write("""
    Il progetto appare interessante perché unisce tre elementi:
    
    1. acquisto sotto mercato;
    2. possibilità di generare reddito tramite Airbnb;
    3. potenziale rivendita con plusvalenza.
    """)

    st.warning("""
    La raccomandazione definitiva resta subordinata alla verifica di:
    conformità urbanistica/catastale, umidità piano terra, spese condominiali,
    regolamento condominiale e condizioni reali del mutuo.
    """)

st.caption("REIA PRO v1.1 - Caso studio Via Capuana 58, Rho.")
