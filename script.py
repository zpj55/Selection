# -*- coding: utf-8 -*-
import math
import random
import hashlib
import pandas as pd
import streamlit as st

# ================== CONFIG ==================
st.set_page_config(page_title="AUDIT2000 – Sélection Aléatoire (ATH Disco)", layout="centered")

# ================== STYLES ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');
* { font-family: 'Comic Neue', cursive !important; }
html, body, .main { background: radial-gradient(circle at 20% 10%, #000, #0a0a0a 60%, #111 100%) !important; }

/* Bandeau */
.blinker {
  position: sticky; top: 0; z-index: 9999;
  text-align: center; padding: 10px 10px; margin-bottom: 8px;
  background: repeating-linear-gradient(45deg, #290000, #290000 10px, #5a0000 10px, #5a0000 20px);
  border: 4px double #ffea00; border-radius: 12px;
  box-shadow: 0 0 18px #ff004d, inset 0 0 12px #ffea00;
  color: #ffea00; font-weight: 900; font-size: 1.3rem;
  animation: blink 1s steps(2, jump-none) infinite;
}
@keyframes blink { 50% { opacity: 0.25; } }

/* === TITRE DISCO ENORME === */
.disco-title {
  font-size: 4.8rem;
  text-align: center;
  font-weight: 900;
  letter-spacing: 6px;
  margin: 30px 0 20px 0;
  text-transform: uppercase;
  background: linear-gradient(90deg, #ff004d, #ffea00, #00ffd5, #bd00ff, #ff004d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 
      0 0 25px #ff004d,
      0 0 45px #ffea00,
      0 0 70px #00ffd5,
      0 0 100px #bd00ff;
  animation: discoPulse 3s ease-in-out infinite, hueRotate 8s linear infinite;
}
@keyframes discoPulse {
  0%,100% { transform: scale(1); filter: brightness(1); }
  50% { transform: scale(1.08); filter: brightness(1.4); }
}
@keyframes hueRotate {
  from { filter: hue-rotate(0deg); }
  to { filter: hue-rotate(360deg); }
}

/* Sous-titre */
.disco-sub {
  text-align: center;
  color: #ffea00;
  font-size: 1.6rem;
  margin-top: -10px;
  text-shadow: 0 0 15px #ffea00;
}

/* Disque rotatif */
.spinner360 {
  width: 120px; height: 120px; border-radius: 50%;
  margin: 16px auto 18px auto;
  background: conic-gradient(#ff004d, #ff7b00, #ffe600, #00ff9d, #00bfff, #bd00ff, #ff004d);
  box-shadow: 0 0 25px #ff004d, 0 0 50px #00bfff;
  animation: spin 2.5s linear infinite, glow 3s ease-in-out infinite;
}
@keyframes spin { to { transform: rotate(360deg);} }
@keyframes glow { 0%,100% { filter: brightness(1);} 50% { filter: brightness(1.4);} }

.block {
  background: #070707; border: 3px dashed #ff00d4; border-radius: 16px;
  box-shadow: 0 0 20px rgba(255,0,212,0.35), inset 0 0 12px rgba(255,234,0,0.25);
  padding: 14px; margin-bottom: 10px;
}
.stButton > button {
  font-size: 1.15rem !important; padding: 10px 16px !important; border-radius: 14px !important;
  border: 4px solid #ffea00 !important; color: #111 !important;
  background: linear-gradient(135deg, #ff004d, #ffe600) !important;
  box-shadow: 0 0 18px #ff004d !important;
  font-weight: 700;
}
.label { color: #00ffcc; text-shadow: 0 0 6px #00ffcc; font-size: 1.05rem; }
.result {
  text-align: center; font-size: 2.2rem; font-weight: 900; padding: 12px;
  border-radius: 16px; border: 4px dotted #00ffd5;
  color: #00ffd5; background: #001b1a; box-shadow: 0 0 22px #00ffd5;
}
.footer { text-align:center; color:#999; font-size:0.95rem; margin-top: 18px;}
.marquee {
  overflow: hidden; white-space: nowrap; border: 2px solid #ff00d4; border-radius: 10px; padding: 4px 8px; color: #ff00d4;
}
.marquee span { display: inline-block; padding-left: 100%; animation: marquee 14s linear infinite; }
@keyframes marquee { 0% { transform: translate(0,0); } 100% { transform: translate(-100%,0);} }
</style>
""", unsafe_allow_html=True)

# ================== EN-TÊTE DISCO ==================
st.markdown('<div class="blinker">🚨 AUDIT2000 — H2A Mood Driven 🚨</div>', unsafe_allow_html=True)
st.markdown('<div class="spinner360"></div>', unsafe_allow_html=True)
st.markdown('<div class="disco-title">SÉLECTION ALÉATOIRE — TYPE ATH</div>', unsafe_allow_html=True)
st.markdown('<div class="disco-sub">(mais en mieux, évidemment)</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ffd700;margin-top:8px;'>L’outil officiel de tirage aléatoire made in H2A — entre humour, seed, et rigueur cosmique.</p>", unsafe_allow_html=True)

# ================== CHOIX ==================
MOTIVATION = ["Faible", "Moyen", "Fort"]
ENT_SYMPA = ["Oui", "Non"]
H2A_VIEW = ["Très bonne organisation de protection", "Très sympa", "Organisation terroriste"]
FRAUDE = ["Oui", "Non", "Oui mais t’inquiète c pa grave"]

st.markdown('<div class="block">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    motivation = st.radio("🔥 Motivation initiale de l’auditeur", MOTIVATION, index=1)
    sympa = st.radio("😊 L’entreprise auditée a été sympa ?", ENT_SYMPA, index=0)
with c2:
    h2a_view = st.radio("🛡️ Perception de la H2A", H2A_VIEW, index=0)
    fraude = st.radio("🕵️ La société auditée fraude ?", FRAUDE, index=1)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="block">', unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    population = st.slider("Population totale", 100, 100_000, 10_000, 100)
    risque = st.selectbox("Niveau de risque perçu", ["Faible","Modéré","Élevé","Apocalyptique"], index=1)
with c4:
    mater = st.slider("Matérialité (plus faible ⇒ N ↑)", 0.1, 10.0, 2.5, 0.1)
    ambiance = st.selectbox("Ambiance visuelle", ["Sobre","Disco","Apocalypse"], index=1)
st.markdown('</div>', unsafe_allow_html=True)

# ================== CALCUL ==================
def _hash_seed(*parts) -> int:
    s = "||".join([str(p).strip().upper() for p in parts])
    return int(hashlib.sha256(s.encode()).hexdigest(), 16) % (2**32)

def _factor(x, d): return d.get(x, 1.0)
def compute_n(pop, risk, materiality, motiv, nice, h2a, fraud) -> tuple[int, int]:
    f = {
        "risk": {"Faible": 0.8, "Modéré": 1.0, "Élevé": 1.4, "Apocalyptique": 2.0},
        "motiv": {"Faible": 0.8, "Moyen": 1.0, "Fort": 1.25},
        "nice": {"Oui": 0.9, "Non": 1.15},
        "h2a": {"Très bonne organisation de protection": 1.0, "Très sympa": 0.95, "Organisation terroriste": 1.35},
        "fraud": {"Non": 0.85, "Oui": 1.35, "Oui mais t’inquiète c pa grave": 1.15}
    }
    base = max(5, int(0.6 * math.sqrt(pop)))
    scale = _factor(risk, f["risk"]) * _factor(motiv, f["motiv"]) * _factor(nice, f["nice"]) * _factor(h2a, f["h2a"]) * _factor(fraud, f["fraud"]) / (max(0.15, min(materiality, 10.0)) ** 0.6)
    n = int(round(base * scale))
    n = max(5, min(n, int(0.15 * pop)))
    return n, _hash_seed(pop, risk, materiality, motiv, nice, h2a, fraud)

# ================== ACTION ==================
colA, colB = st.columns(2)
with colA:
    if st.button("🎯 Calculer le N"):
        N, seed = compute_n(population, risque, mater, motivation, sympa, h2a_view, fraude)
        if ambiance == "Disco": st.balloons()
        if ambiance == "Apocalypse": st.snow()
        st.markdown(f"<div class='result'>NOMBRE À TIRER = <strong>{N}</strong></div>", unsafe_allow_html=True)
        st.session_state["_N"], st.session_state["_seed"] = N, seed
        st.code(f"Seed = {seed}")

with colB:
    if st.button("🧪 Tirer un échantillon"):
        if "_N" not in st.session_state:
            st.warning("D’abord, calculez le N !")
        else:
            random.seed(st.session_state["_seed"])
            N = st.session_state["_N"]
            sample = sorted(random.sample(range(1, population+1), N))
            df = pd.DataFrame({"ID CONTRÔLE": sample})
            st.dataframe(df, use_container_width=True, height=260)
            st.download_button("💾 Télécharger CSV", df.to_csv(index=False).encode(), "echantillon_disco.csv", "text/csv")

st.markdown("<div class='footer'>© 2025 AUDIT2000 – H2A Mood Driven – Sélection aléatoire type ATH (mais avec plus de groove)</div>", unsafe_allow_html=True)
