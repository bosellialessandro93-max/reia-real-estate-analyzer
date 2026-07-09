import numpy_financial as npf


def euro(value: float) -> str:
    return f"{value:,.0f} €".replace(",", ".")


def pct(value: float) -> str:
    return f"{value:.1f}%"


def calculate_investment(data: dict) -> dict:
    investimento_base = (
        data["prezzo_acquisto"]
        + data["ristrutturazione"]
        + data["arredo"]
    )

    investimento_totale = investimento_base + data["spese_acquisto"]
    costo_mq = investimento_totale / data["mq"]

    mutuo = investimento_totale * (1 - data["anticipo_pct"] / 100)
    capitale_iniziale = investimento_totale * (data["anticipo_pct"] / 100)

    if mutuo > 0:
        rata_mensile = -npf.pmt(
            data["tasso"] / 100 / 12,
            data["durata_anni"] * 12,
            mutuo
        )
    else:
        rata_mensile = 0

    rata_annua = rata_mensile * 12

    notti_anno = 365 * data["occupazione"] / 100
    ricavi_lordi = notti_anno * data["adr"]
    costi_operativi = ricavi_lordi * data["costi_operativi_pct"] / 100
    noi = ricavi_lordi - costi_operativi
    tasse = noi * data["tassazione_pct"] / 100

    cash_flow_pre_tasse = noi - rata_annua
    cash_flow_netto = noi - rata_annua - tasse

    valore_attuale = data["valore_rivendita_mq"] * data["mq"]
    valore_futuro = valore_attuale * ((1 + data["crescita_annua"] / 100) ** data["anni_exit"])

    capital_gain = valore_futuro - investimento_totale
    margin_of_safety = valore_attuale - investimento_totale

    roi_lordo = (noi / investimento_totale) * 100
    roi_netto = (cash_flow_netto / investimento_totale) * 100
    cash_on_cash = (cash_flow_netto / capitale_iniziale * 100) if capitale_iniziale > 0 else 0

    reia_score = calculate_reia_score(
        costo_mq=costo_mq,
        investimento_totale=investimento_totale,
        valore_attuale=valore_attuale,
        roi_lordo=roi_lordo,
        cash_flow_netto=cash_flow_netto,
        capital_gain=capital_gain,
        posizione_score=data["posizione_score"],
        rischio_score=data["rischio_score"],
        airbnb_score=data["airbnb_score"],
        stato_score=data["stato_score"],
    )

    return {
        "investimento_base": investimento_base,
        "investimento_totale": investimento_totale,
        "costo_mq": costo_mq,
        "mutuo": mutuo,
        "capitale_iniziale": capitale_iniziale,
        "rata_mensile": rata_mensile,
        "rata_annua": rata_annua,
        "notti_anno": notti_anno,
        "ricavi_lordi": ricavi_lordi,
        "costi_operativi": costi_operativi,
        "noi": noi,
        "tasse": tasse,
        "cash_flow_pre_tasse": cash_flow_pre_tasse,
        "cash_flow_netto": cash_flow_netto,
        "valore_attuale": valore_attuale,
        "valore_futuro": valore_futuro,
        "capital_gain": capital_gain,
        "margin_of_safety": margin_of_safety,
        "roi_lordo": roi_lordo,
        "roi_netto": roi_netto,
        "cash_on_cash": cash_on_cash,
        "reia_score": reia_score["score"],
        "score_details": reia_score["details"],
        "verdict": reia_score["verdict"],
    }


def calculate_reia_score(
    costo_mq: float,
    investimento_totale: float,
    valore_attuale: float,
    roi_lordo: float,
    cash_flow_netto: float,
    capital_gain: float,
    posizione_score: int,
    rischio_score: int,
    airbnb_score: int,
    stato_score: int,
) -> dict:
    score_prezzo = min(100, max(0, (1800 / costo_mq) * 60))
    score_valore = min(100, max(0, 50 + ((valore_attuale - investimento_totale) / investimento_totale) * 50))
    score_redditivita = min(100, max(0, roi_lordo * 10))
    score_cashflow = min(100, max(0, 50 + cash_flow_netto / 250))
    score_capital_gain = min(100, max(0, 50 + capital_gain / 1000))

    final_score = (
        score_prezzo * 0.20
        + score_valore * 0.15
        + score_redditivita * 0.15
        + score_cashflow * 0.15
        + score_capital_gain * 0.15
        + posizione_score * 0.08
        + rischio_score * 0.05
        + airbnb_score * 0.04
        + stato_score * 0.03
    )

    final_score = round(final_score, 1)

    if final_score >= 90:
        verdict = "Opportunità eccezionale"
    elif final_score >= 85:
        verdict = "Investimento molto interessante"
    elif final_score >= 80:
        verdict = "Buon investimento"
    elif final_score >= 70:
        verdict = "Da approfondire / negoziare"
    else:
        verdict = "Elevata attenzione"

    return {
        "score": final_score,
        "verdict": verdict,
        "details": {
            "Prezzo": round(score_prezzo, 1),
            "Valore reale": round(score_valore, 1),
            "Redditività": round(score_redditivita, 1),
            "Cash Flow": round(score_cashflow, 1),
            "Capital Gain": round(score_capital_gain, 1),
            "Posizione": posizione_score,
            "Rischio": rischio_score,
            "Airbnb": airbnb_score,
            "Stato immobile": stato_score,
        }
    }
