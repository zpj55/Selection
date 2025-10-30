# -*- coding: utf-8 -*-
import math
import random
import hashlib
import pandas as pd
import streamlit as st

# ================== CONFIG ==================
st.set_page_config(page_title="AUDIT2000 – Sélection Aléatoire (ATH++)", layout="centered")

# ================== STYLES ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');
* { font-family: 'Comic Neue', cursive !important; }
html, body, .main { background: radial-gradient(circle at 20% 10%, #0a0a0a, #111 60%, #000 100%) !important; }

/* Bandeau */
.blinker {
  position: sticky; top: 0; z-index: 9999;
  text-align: center; padding: 8px 10px; margin-bottom: 8px;
  background: repeating-linear-gradient(45deg, #2a0000, #2a0000 10px, #5a0000 10px, #5a0000 20px);
  border: 4px double #ffea00; border-radius: 12px;
  box-shadow: 0 0 18px #ff004d, inset 0 0 12px #ffea00;
  color: #ffea00; font-weight: 900; font-size: 1.2rem;
  animation: blink 1s steps(2, jump-none) infinite;
}
@keyframes blink { 50% { opacity: 0.25; } }

/* Titre */
.kitsch-title {
  font-size: 2.6rem; text-align: center; letter-spacing: 2px;
  background: linear-gradient(90deg, #ff004d, #ffea00, #00ffd5, #bd00ff, #ff004d);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px #ff004d, 0 0 40px #ffea00, 0 0 60px #00ffd5;
  margin: 12px 0 6px 0;
}

/* Disque 360° */
.spinner360 {
  width: 90px; height: 90px; border-radius: 50%;
  margin: 6px auto 10px auto;
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
  font-size: 1.15rem !important; padding: 10px 16px !important; border-radius: 14px !important;
  border: 4px solid #ffea00 !important; color: #111 !important;
  background: linear-gradient(135deg, #ff004d, #ffe600) !important;
  box-shadow: 0 0 18px #ff004d !important;
}
.label { color: #00ffcc; text-shadow: 0 0 6px #00ffcc; font-size: 1.05rem; }
.result {
  text-align: center; font-size: 1.9rem; font-weight: 900; padding: 12px;
  border-radius: 16px; border: 4px dotted #00ffd5;
  color: #00ffd5; background: #001b1a; box-shadow: 0 0 22px #00ffd5;
}
.footer { text-align:center; color:#999; font-size:0.95rem; margin-top: 18px;}
.badges { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin: 6px 0 10px 0; }
.badge {
  display:inline-block; padding:4px 8px; border-radius:10px; font-weight:700;
  border:2px solid #ffea00; color:#111; background:#ffe600;
}
.marquee {
  overflow: hidden; white-space: nowrap; border: 2px solid #ff00d4; border-radius: 10px; padding: 4px 8px; color: #ff00d4;
}
.marquee span { display: inline-block; padding-left: 100%; animation: marquee 14s linear infinite; }
@keyframes marquee { 0% { transform: translate(0,0); } 100% { transform: translate(-100%,0);} }
</style>
""", unsafe_allow_html=True)

# ================== EN-TÊTE ==================
st.markdown('<div class="blinker">✨🚨 AUDIT2000 — Sélection aléatoire transparente (type ATH), mais en mieux 🚨✨</div>', unsafe_allow_html=True)
st.markdown('<div class="spinner360"></div>', unsafe_allow_html=True)
st.markdown('<div class="kitsch-title">H2A-9000 — ATH++ Random Selector</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ffd700;margin-top:-6px;'>"
            "Sélection <strong>100% aléatoire</strong> avec traçabilité : seed, paramètres, empreinte de tirage."
            "</p>", unsafe_allow_html=True)
st.markdown('<div class="badges"><span class="badge">Aléa contrôlé</span><span class="badge">Seed traçable</span><span class="badge">Export CSV</span></div>', unsafe_allow_html=True)

# ================== CHOIX DEMANDÉS ==================
MOTIVATION = ["Faible", "Moyen", "Fort"]
ENT_SYMPA = ["Oui", "Non"]
H2A_VIEW = ["Très bonne organisation de protection", "Très sympa", "Organisation terroriste"]
FRAUDE = ["Oui", "Non", "Oui mais t’inquiète c pa grave"]
RNG_MODE = ["Pseudo-aléatoire (seed)", "Aléa système (OS)"]

st.markdown('<div class="block">', unsafe_allow_html=True)
c0, = st.columns(1)
with c0:
    rng_mode = st.radio("Mode de tirage aléatoire", RNG_MODE, index=0, horizontal=True)

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

# ================== OPTIONS SUPPLÉMENTAIRES (sans champ libre) ==================
st.markdown('<div class="block">', unsafe_allow_html=True)
st.markdown('<div class="label">⚙️ Options supplémentaires</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    population = st.slider("Population totale", 100, 100_000, 10_000, 100)
    risque = st.selectbox("Niveau de risque perçu", ["Faible","Modéré","Élevé","Apocalyptique"], index=1)
with c4:
    mater = st.slider("Matérialité (plus faible ⇒ N ↑)", 0.1, 10.0, 2.5, 0.1)
    ambiance = st.selectbox("Ambiance visuelle", ["Sobre","Disco","Apocalypse"], index=1)

fix_seed = st.toggle("🔐 Graine déterministe (rejouable) — seulement pour ‘Pseudo-aléatoire (seed)’", value=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="marquee"><span>⚠️ Outil de sélection aléatoire (type ATH). Le modèle de calcul du N est volontairement ludique. Le tirage, lui, est réellement aléatoire.</span></div>', unsafe_allow_html=True)

# ================== CALCUL ==================
def _hash_seed(*parts) -> int:
    s = "||".join([str(p).strip().upper() for p in parts])
    return int(hashlib.sha256(s.encode()).hexdigest(), 16) % (2**32)

def _risk_factor(level: str) -> float:
    return {"Faible": 0.8, "Modéré": 1.0, "Élevé": 1.4, "Apocalyptique": 2.0}.get(level, 1.0)

def _motivation_factor(level: str) -> float:
    return {"Faible": 0.8, "Moyen": 1.0, "Fort": 1.25}.get(level, 1.0)

def _sympa_factor(val: str) -> float:
    return {"Oui": 0.9, "Non": 1.15}.get(val, 1.0)

def _h2a_factor(val: str) -> float:
    return {
        "Très bonne organisation de protection": 1.00,
        "Très sympa": 0.95,
        "Organisation terroriste": 1.35
    }.get(val, 1.0)

def _fraude_factor(val: str) -> float:
    return {
        "Non": 0.85,
        "Oui": 1.35,
        "Oui mais t’inquiète c pa grave": 1.15
    }.get(val, 1.0)

def compute_n(pop, risk, materiality, motiv, nice, h2a, fraud) -> tuple[int, int, str]:
    base = max(5, int(0.6 * math.sqrt(pop)))  # base ludique
    scale = (
        _risk_factor(risk)
        * _motivation_factor(motiv)
        * _sympa_factor(nice)
        * _h2a_factor(h2a)
        * _fraude_factor(fraud)
        / (max(0.15, min(materiality, 10.0)) ** 0.6)
    )
    n_raw = int(round(base * scale))
    n = max(5, min(n_raw, max(5, int(0.15 * pop))))  # plafond 15%
    seed_int = _hash_seed(pop, risk, materiality, motiv, nice, h2a, fraud)
    seed_str = f"{pop}|{risk}|{materiality}|{motiv}|{nice}|{h2a}|{fraud}"
    return n, seed_int, seed_str

def sample_ids(pop_size: int, n: int, rng_kind: str, seed_int: int | None):
    if rng_kind == "Aléa système (OS)":
        sysrng = random.SystemRandom()
        population_list = list(range(1, pop_size + 1))
        n_effectif = min(n, pop_size)
        return sorted(sysrng.sample(population_list, n_effectif))
    else:
        if seed_int is not None:
            random.seed(seed_int)
        population_list = list(range(1, pop_size + 1))
        n_effectif = min(n, pop_size)
        return sorted(random.sample(population_list, n_effectif))

def hash_sample(sample_list, seed_str: str) -> str:
    """Empreinte de tirage (traçabilité): hash(seed_str + sample_csv)."""
    joined = ",".join(map(str, sample_list))
    payload = (seed_str + "||" + joined).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

# ================== ACTIONS ==================
colA, colB = st.columns(2)
with colA:
    if st.button("🎯 Calculer le N (affichage officiel)"):
        N, seed_int, seed_str = compute_n(population, risque, mater, motivation, sympa, h2a_view, fraude)

        if rng_mode == "Pseudo-aléatoire (seed)" and fix_seed:
            random.seed(seed_int)

        if ambiance == "Disco":
            st.balloons()
        elif ambiance == "Apocalypse":
            st.snow()

        st.toast("N calculé. Tirage aléatoire conforme au mode choisi (ATH++).", icon="✅")
        st.markdown("---")
        st.markdown(f"<div class='result'>NOMBRE À TIRER = <strong>{N}</strong></div>", unsafe_allow_html=True)

        with st.expander("Traçabilité & paramètres (ATH++)"):
            st.code(f"Mode RNG = {rng_mode}")
            st.code(f"Pop={population}, Risque={risque}, Matérialité={mater}")
            st.code(f"Motivation={motivation}, Sympa={sympa}, H2A={h2a_view}, Fraude={fraude}")
            if rng_mode == "Pseudo-aléatoire (seed)":
                st.code(f"Seed (int) = {seed_int}")
                st.code(f"Seed (str) = {seed_str}")
            else:
                st.info("Mode ‘Aléa système (OS)’ : pas de seed réutilisable (tirage non reproductible).")

            st.markdown("**Pourquoi “comme ATH, mais en mieux” ?**")
            st.markdown(
                "- Tirage **réellement aléatoire** (seedé ou via l’aléa système OS).\n"
                "- **Traçabilité** : paramètres affichés, seed, empreinte SHA-256 du tirage.\n"
                "- **Export CSV** immédiat et justificatif interne clair."
            )

        st.session_state["_lastN"] = N
        st.session_state["_last_seed_int"] = seed_int
        st.session_state["_last_seed_str"] = seed_str
        st.session_state["_last_rng_mode"] = rng_mode
        st.session_state["_pop"] = population

with colB:
    if st.button("🧪 Tirer un échantillon (aléatoire)"):
        if "_lastN" not in st.session_state:
            st.warning("Commencez par calculer le N.")
        else:
            N = st.session_state["_lastN"]
            seed_int = st.session_state.get("_last_seed_int", None)
            seed_str = st.session_state.get("_last_seed_str", "")
            rng_mode_last = st.session_state.get("_last_rng_mode", rng_mode)
            pop_now = st.session_state.get("_pop", population)

            # Tirage selon le mode choisi au moment du calcul
            sample = sample_ids(pop_now, N, rng_mode_last, seed_int if (rng_mode_last.startswith("Pseudo") and fix_seed) else None)
            df = pd.DataFrame({"ID CONTRÔLE": sample})

            # Empreinte de tirage (preuve)
            imprint = hash_sample(sample, seed_str if rng_mode_last.startswith("Pseudo") else "OS_MODE")

            st.markdown("---")
            st.markdown("<div class='block'>", unsafe_allow_html=True)
            st.markdown(
                f"**Échantillon généré** — taille {len(sample)} "
                f"— RNG: `{rng_mode_last}` "
                + (f"— seed: `{seed_int}`" if rng_mode_last.startswith("Pseudo") and fix_seed else "— seed: N/A (OS)"),
                unsafe_allow_html=True
            )
            st.code(f"Empreinte SHA-256 du tirage = {imprint}")

            st.dataframe(df, use_container_width=True, height=260)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("💾 Télécharger CSV", csv, file_name="echantillon_audit2000.csv", mime="text/csv")
            st.markdown("</div>", unsafe_allow_html=True)

# ================== FAQ / ENCADRÉ ==================
with st.expander("FAQ — Ce que cela prouve / ne prouve pas"):
    st.markdown(
        "- ✅ **Sélection aléatoire** : les IDs sont tirés au hasard (seedé ou via aléa système).\n"
        "- ✅ **Traçabilité** : vous pouvez re-faire le tirage seedé et vérifier l’empreinte.\n"
        "- ⚠️ **Le calcul du N** est volontairement ludique (mood-driven). Le **tirage**, lui, est sérieux."
    )

# ================== PIED DE PAGE ==================
st.markdown("<div class='footer'>© 2025 AUDIT2000 — Sélection Aléatoire (ATH++) "
            "• Pour les puristes : utilisez le mode “Aléa système (OS)” ou la seed pour rejouer.</div>",
            unsafe_allow_html=True)
