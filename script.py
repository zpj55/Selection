# -*- coding: utf-8 -*-
import math
import random
import hashlib
import pandas as pd
import streamlit as st

# ================== CONFIG ==================
st.set_page_config(page_title="AUDIT2000 – H2A Mood Driven", layout="centered")

# ================== STYLES ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');
* { font-family: 'Comic Neue', cursive !important; }
html, body, .main { background: radial-gradient(circle at 20% 10%, #0a0a0a, #111 60%, #000 100%) !important; }

/* Bandeau AUDIT2000 */
.blinker {
  position: sticky; top: 0; z-index: 9999;
  text-align: center; padding: 8px 10px; margin-bottom: 8px;
  background: repeating-linear-gradient(45deg, #2a0000, #2a0000 10px, #5a0000 10px, #5a0000 20px);
  border: 4px double #ffea00; border-radius: 12px;
  box-shadow: 0 0 18px #ff004d, inset 0 0 12px #ffea00;
  color: #ffea00; font-weight: 900; font-size: 1.6rem;
  animation: blink 1s steps(2, jump-none) infinite;
}
@keyframes blink { 50% { opacity: 0.25; } }

/* Titre */
.kitsch-title {
  font-size: 3.8rem; text-align: center; letter-spacing: 4px;
  background: linear-gradient(90deg, #ff004d, #ffea00, #00ffd5, #bd00ff, #ff004d);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px #ff004d, 0 0 40px #ffea00, 0 0 60px #00ffd5;
  animation: hueShift 5s linear infinite, pop 2.2s ease-in-out infinite;
  margin: 14px 0 6px 0;
}
@keyframes hueShift { from { filter: hue-rotate(0deg);} to { filter: hue-rotate(360deg);} }
@keyframes pop { 0%,100% { transform: scale(1);} 50% { transform: scale(1.05);} }

/* Disque 360° */
.spinner360 {
  width: 110px; height: 110px; border-radius: 50%;
  margin: 8px auto 10px auto;
  background: conic-gradient(#ff004d, #ff7b00, #ffe600, #00ff9d, #00bfff, #bd00ff, #ff004d);
  box-shadow: 0 0 25px #ff004d, 0 0 50px #00bfff;
  animation: spin 2.5s linear infinite, glow 3s ease-in-out infinite;
}
@keyframes spin { to { transform: rotate(360deg);} }
@keyframes glow { 0%,100% { filter: brightness(1);} 50% { filter: brightness(1.35);} }

.block {
  background: #070707; border: 3px dashed #ff00d4; border-radius: 16px;
  box-shadow: 0 0 20px rgba(255,0,212,0.35), inset 0 0 12px rgba(255,234,0,0.25);
  padding: 14px; margin-bottom: 10px;
}
.stButton > button {
  font-size: 1.3rem !important; padding: 10px 16px !important; border-radius: 14px !important;
  border: 4px solid #ffea00 !important; color: #111 !important;
  background: linear-gradient(135deg, #ff004d, #ffe600) !important;
  box-shadow: 0 0 18px #ff004d !important;
  animation: wobble 2.4s ease-in-out infinite;
}
@keyframes wobble { 0%,100% { transform: rotate(0deg);} 25% { transform: rotate(-2deg);} 75% { transform: rotate(2deg);} }

.label { color: #00ffcc; text-shadow: 0 0 6px #00ffcc; font-size: 1.05rem; }
.result {
  text-align: center; font-size: 2.3rem; font-weight: 900; padding: 12px;
  border-radius: 16px; border: 4px dotted #00ffd5;
  color: #00ffd5; background: #001b1a; box-shadow: 0 0 22px #00ffd5;
}
.footer { text-align:center; color:#777; font-size:0.95rem; margin-top: 18px;}
.marquee {
  overflow: hidden; white-space: nowrap; border: 2px solid #ff00d4; border-radius: 10px; padding: 4px 8px; color: #ff00d4;
  animation: shadowPulse 2.5s ease-in-out infinite;
}
.marquee span { display: inline-block; padding-left: 100%; animation: marquee 14s linear infinite; }
@keyframes marquee { 0% { transform: translate(0,0); } 100% { transform: translate(-100%,0);} }
@keyframes shadowPulse { 0%,100% { box-shadow: 0 0 10px #ff00d4;} 50% { box-shadow: 0 0 22px #ff00d4;} }
</style>
""", unsafe_allow_html=True)

# ================== EN-TÊTE ==================
st.markdown('<div class="blinker">✨🚨 AUDIT2000 🚨✨ — H2A Mood Driven — Merci de ne jamais citer ceci en comité d’audit</div>', unsafe_allow_html=True)
st.markdown('<div class="spinner360"></div>', unsafe_allow_html=True)
st.markdown('<div class="kitsch-title">H2A-9000 — Mood Driven</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ffd700;margin-top:-6px;'>Le <strong>Nombre à Tirer</strong> déterminé par l’humeur, la politesse et un soupçon d’absurde.</p>", unsafe_allow_html=True)

# ================== CHOIX DEMANDÉS ==================
MOTIVATION = ["Faible", "Moyen", "Fort"]
ENT_SYMPA = ["Oui", "Non"]
H2A_VIEW = ["Très bonne organisation de protection", "Très sympa", "Organisation terroriste"]
FRAUDE = ["Oui", "Non", "Oui mais t’inquiète c pa grave"]

st.markdown('<div class="block">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="label">🔥 Motivation initiale de l’auditeur</div>', unsafe_allow_html=True)
    motivation = st.radio("Motivation", MOTIVATION, index=1)

    st.markdown('<div class="label">😊 L’entreprise auditée a été sympa ?</div>', unsafe_allow_html=True)
    sympa = st.radio("Entreprise sympa", ENT_SYMPA, index=0)

with c2:
    st.markdown('<div class="label">🛡️ Comment percevez-vous la H2A ?</div>', unsafe_allow_html=True)
    h2a_view = st.radio("Perception H2A", H2A_VIEW, index=0)

    st.markdown('<div class="label">🕵️ La société auditée fraude ?</div>', unsafe_allow_html=True)
    fraude = st.radio("Fraude ?", FRAUDE, index=1)

st.markdown('</div>', unsafe_allow_html=True)

# ================== OPTIONS SUPPLÉMENTAIRES (toujours sans champ libre) ==================
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown('<div class="label">⚙️ Options supplémentaires (facultatives)</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    population = st.slider("Population totale", 100, 100_000, 10_000, 100)
    risque = st.selectbox("Niveau de risque perçu", ["Faible","Modéré","Élevé","Apocalyptique"], index=1)
with c4:
    mater = st.slider("Matérialité (plus faible ⇒ N ↑)", 0.1, 10.0, 2.5, 0.1)
    ambiance = st.selectbox("Ambiance visuelle", ["Sobre","Disco","Apocalypse"], index=1)
fix_seed = st.toggle("🔐 Graine déterministe (rejouable)", value=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="marquee"><span>⚠️ Ceci n’est PAS une méthode d’échantillonnage réelle. C’est une blague sérieuse, ou l’inverse. ⚠️</span></div>', unsafe_allow_html=True)

# ================== CALCUL ==================
def _hash_seed(*parts) -> int:
    s = "||".join([str(p).strip().upper() for p in parts])
    return int(hashlib.sha256(s.encode()).hexdigest(), 16) % (2**32)

def _risk_factor(level: str) -> float:
    return {"Faible": 0.8, "Modéré": 1.0, "Élevé": 1.4, "Apocalyptique": 2.0}.get(level, 1.0)

def _motivation_factor(level: str) -> float:
    # motivation forte ⇒ on veut “bien faire” ⇒ N ↑
    return {"Faible": 0.8, "Moyen": 1.0, "Fort": 1.25}.get(level, 1.0)

def _sympa_factor(val: str) -> float:
    # entreprise sympa ⇒ on “desserre” un peu ; sinon on serre les dents
    return {"Oui": 0.9, "Non": 1.15}.get(val, 1.0)

def _h2a_factor(val: str) -> float:
    table = {
        "Très bonne organisation de protection": 1.00,
        "Très sympa": 0.95,
        "Organisation terroriste": 1.35,  # on se blinde…
    }
    return table.get(val, 1.0)

def _fraude_factor(val: str) -> float:
    table = {
        "Non": 0.85,
        "Oui": 1.35,
        "Oui mais t’inquiète c pa grave": 1.15,  # “grave pas grave”… on augmente quand même.
    }
    return table.get(val, 1.0)

def compute_n(pop, risk, materiality, motiv, nice, h2a, fraud) -> tuple[int, int]:
    base = max(5, int(0.6 * math.sqrt(pop)))  # base arbitraire
    scale = (
        _risk_factor(risk)
        * _motivation_factor(motiv)
        * _sympa_factor(nice)
        * _h2a_factor(h2a)
        * _fraude_factor(fraud)
        / (max(0.15, min(materiality, 10.0)) ** 0.6)
    )
    n_raw = int(round(base * scale))
    n = max(5, min(n_raw, max(5, int(0.15 * pop))))  # plafond 15% population
    seed = _hash_seed(pop, risk, materiality, motiv, nice, h2a, fraud)
    return n, seed

# ================== ACTIONS ==================
colA, colB = st.columns(2)
with colA:
    if st.button("🎯 Calculer le N à tirer (OFFICIELLEMENT)"):
        N, seed = compute_n(population, risque, mater, motivation, sympa, h2a_view, fraude)
        if fix_seed: random.seed(seed)
        if ambiance == "Disco": st.balloons()
        if ambiance == "Apocalypse": st.snow()
        st.toast("Nombre à tirer calculé (méthode 100% mood-driven).", icon="✅")
        st.markdown("---")
        st.markdown(f"<div class='result'>NOMBRE À TIRER = <strong>{N}</strong></div>", unsafe_allow_html=True)
        with st.expander("Détails (avouez que ça vous rassure)"):
            st.code(f"Pop={population}, Risque={risque}, Matérialité={mater}")
            st.code(f"Motivation={motivation}, Sympa={sympa}, H2A={h2a_view}, Fraude={fraude}")
            st.code(f"Seed = {seed}")
        st.session_state["_lastN"] = N
        st.session_state["_lastSeed"] = seed
        st.session_state["_pop"] = population

with colB:
    if st.button("🧪 Tirer un échantillon (si vous insistez)"):
        if "_lastN" not in st.session_state:
            st.warning("Commencez par calculer le N.")
        else:
            N = st.session_state["_lastN"]
            seed = st.session_state.get("_lastSeed", _hash_seed("fallback"))
            pop_now = st.session_state.get("_pop", population)
            if fix_seed: random.seed(seed)
            population_list = list(range(1, pop_now + 1))
            n_effectif = min(N, len(population_list))
            sample = sorted(random.sample(population_list, n_effectif))
            df = pd.DataFrame({"ID CONTRÔLE": sample})
            st.markdown("---")
            st.markdown("<div class='block'>", unsafe_allow_html=True)
            st.markdown(f"Échantillon généré (taille {n_effectif}) — seed: <code>{seed}</code>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, height=260)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("💾 Télécharger CSV", csv, file_name="echantillon_audit2000.csv", mime="text/csv")
            st.markdown("</div>", unsafe_allow_html=True)

# ================== PIED DE PAGE ==================
st.markdown("<div class='footer'>© 2025 AUDIT2000 x H2A — Mood Driven Edition. "
            "Si quelqu’un vous demande la base normative, changez de sujet.</div>", unsafe_allow_html=True)
