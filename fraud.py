# ============================================================
# APPLICATION DE DÉTECTION DE FRAUDE — STREAMLIT
# Interface visuelle moderne avec CSS personnalisé
# ============================================================

import streamlit as st   # Framework pour créer des applications web en Python
import pandas as pd      # Pour construire le tableau de données envoyé au modèle
import joblib            # Pour charger le modèle sauvegardé

# ============================================================
# CONFIGURATION DE LA PAGE
# Doit être le PREMIER appel Streamlit du script
# ============================================================
st.set_page_config(
    page_title="Détection de Fraude",   # Titre dans l'onglet du navigateur
    page_icon="🔍",                      # Icône dans l'onglet
    layout="centered"                    # Contenu centré (pas plein écran)
)

# ============================================================
# INJECTION DE CSS PERSONNALISÉ
# Streamlit permet d'injecter du HTML/CSS pour personnaliser l'apparence
# unsafe_allow_html=True est nécessaire pour autoriser le HTML brut
# ============================================================
st.markdown("""
<style>
    /* --- Importation de polices Google --- */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    /* --- Fond principal de l'application --- */
    .stApp {
        background: #080b14;
        background-image:
            linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    /* --- Suppression du padding par défaut du bloc principal --- */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 580px;
    }

    /* --- Texte général en blanc cassé --- */
    html, body, [class*="css"] {
        color: #e2e8f0;
        font-family: 'DM Sans', sans-serif;
    }

    /* --- Étiquettes des champs (labels) --- */
    label, .stSelectbox label, .stNumberInput label {
        color: rgba(255,255,255,0.45) !important;
        font-size: 11px !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        font-weight: 500 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* --- Champs de saisie numérique et listes déroulantes --- */
    .stNumberInput input,
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 18px !important;
        transition: border-color 0.2s !important;
    }

    /* --- Effet au survol des champs --- */
    .stNumberInput input:focus,
    .stSelectbox > div > div:focus {
        border-color: rgba(99,102,241,0.6) !important;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.15) !important;
    }

    /* --- Bouton principal "Analyser" --- */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 24px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        font-family: 'DM Sans', sans-serif !important;
        letter-spacing: 0.04em !important;
        cursor: pointer !important;
        box-shadow: 0 4px 24px rgba(99,102,241,0.3) !important;
        transition: all 0.25s !important;
        margin-top: 8px !important;
    }

    /* --- Effet au survol du bouton --- */
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(99,102,241,0.45) !important;
    }

    /* --- Suppression du fond blanc des blocs Streamlit --- */
    .stAlert {
        border-radius: 16px !important;
    }

    /* --- Ligne de séparation horizontale --- */
    hr {
        border-color: rgba(255,255,255,0.07) !important;
        margin: 1.5rem 0 !important;
    }

    /* --- Fond de la barre latérale (si activée) --- */
    section[data-testid="stSidebar"] {
        background: #0d1021;
    }

    /* --- Texte du sélecteur déroulant --- */
    .stSelectbox [data-baseweb="select"] span {
        color: #f1f5f9 !important;
        font-family: 'DM Mono', monospace !important;
    }

    /* --- Dropdown ouvert --- */
    [data-baseweb="popover"] {
        background: #111827 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
    }

    [data-baseweb="menu"] li {
        color: #e2e8f0 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    [data-baseweb="menu"] li:hover {
        background: rgba(99,102,241,0.15) !important;
    }

    /* --- Masquer le menu hamburger et le footer Streamlit --- */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CHARGEMENT DU MODÈLE
# On charge le pipeline (prétraitement + modèle) depuis le fichier .pkl
# @st.cache_resource évite de recharger le modèle à chaque interaction
# ============================================================
@st.cache_resource
def load_model():
    return joblib.load("fraud_detection_pipeline.pkl")

model = load_model()

# ============================================================
# EN-TÊTE DE L'APPLICATION
# Utilisation de HTML personnalisé pour un rendu plus soigné
# ============================================================

# Badge "Système actif" en haut
st.markdown("""
<div style="display:flex; justify-content:center; margin-bottom:20px;">
    <div style="
        display:inline-flex; align-items:center; gap:8px;
        background:rgba(99,102,241,0.1);
        border:1px solid rgba(99,102,241,0.3);
        border-radius:100px; padding:6px 18px;">
        <div style="
            width:7px; height:7px; border-radius:50%;
            background:#6366f1; box-shadow:0 0 8px #6366f1;">
        </div>
        <span style="
            font-size:11px; color:rgba(255,255,255,0.55);
            letter-spacing:0.1em; text-transform:uppercase;
            font-family:'DM Sans',sans-serif;">
            Système de détection actif
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Titre principal avec dégradé de couleur
st.markdown("""
<div style="text-align:center; margin-bottom:10px;">
    <h1 style="
        font-family:'Playfair Display',serif;
        font-size:clamp(28px,5vw,40px);
        color:#f8fafc; line-height:1.2; margin-bottom:10px;">
        Détection de
        <span style="
            background:linear-gradient(135deg,#6366f1,#ef4444);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;">
            Fraude
        </span>
    </h1>
    <p style="color:rgba(255,255,255,0.35); font-size:14px; line-height:1.7;
              font-family:'DM Sans',sans-serif;">
        Entrez les détails de la transaction pour analyser le risque de fraude
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================
# SECTION 1 : TYPE DE TRANSACTION
# selectbox = menu déroulant avec les options possibles
# ============================================================
st.markdown('<p style="font-size:11px;color:rgba(255,255,255,0.35);letter-spacing:0.1em;text-transform:uppercase;font-weight:500;margin-bottom:4px;font-family:\'DM Sans\',sans-serif;">Type de transaction</p>', unsafe_allow_html=True)

# Dictionnaire des icônes associées à chaque type de transaction
type_icons = {
    "PAYMENT":  "💳  PAYMENT",
    "TRANSFER": "🔁  TRANSFER",
    "CASH_OUT": "💸  CASH_OUT",
    "DEPOSIT":  "🏦  DEPOSIT"
}

# Menu déroulant pour choisir le type de transaction
# La clé (key) permet à Streamlit d'identifier ce widget de façon unique
transaction_type = st.selectbox(
    label="",                            # On cache le label (déjà affiché manuellement au-dessus)
    options=list(type_icons.values()),   # Options affichées avec icônes
    key="tx_type"
)

# On extrait le vrai type (sans l'icône) pour l'envoyer au modèle
# Ex : "💳  PAYMENT" → "PAYMENT"
clean_type = transaction_type.split("  ")[-1].strip()

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SECTION 2 : MONTANT DE LA TRANSACTION
# Champ numérique avec minimum 0 et valeur par défaut 10 000
# ============================================================

# Affichage de l'icône et du montant formaté en temps réel
st.markdown("""
<p style="font-size:11px;color:rgba(255,255,255,0.35);letter-spacing:0.1em;
text-transform:uppercase;font-weight:500;margin-bottom:4px;
font-family:'DM Sans',sans-serif;">💰 Montant de la transaction</p>
""", unsafe_allow_html=True)

amount = st.number_input(
    label="",
    min_value=0.0,
    value=10000.0,
    step=500.0,           # On avance de 500 en 500 avec les flèches
    format="%.2f",        # Affichage avec 2 décimales
    key="amount"
)

# Affichage du montant mis en forme (avec séparateurs de milliers)
st.markdown(f"""
<div style="
    font-family:'DM Mono',monospace; font-size:13px;
    color:rgba(99,102,241,0.8); margin-top:-10px; margin-bottom:12px;
    padding-left:4px;">
    XAF {amount:,.0f}
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 3 : SOLDES DU COMPTE ÉMETTEUR (celui qui envoie)
# On affiche 2 champs côte à côte grâce à st.columns()
# ============================================================
st.markdown("""
<p style="font-size:11px;color:rgba(255,255,255,0.35);letter-spacing:0.1em;
text-transform:uppercase;font-weight:500;margin-bottom:4px;
font-family:'DM Sans',sans-serif;">📤 Compte émetteur (envoyeur)</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)   # Crée 2 colonnes de largeur égale

with col1:
    # Solde avant la transaction
    oldbalanceOrg = st.number_input(
        "Solde avant",
        min_value=0.0,
        value=10000.0,
        step=100.0,
        format="%.2f",
        key="old_orig"
    )

with col2:
    # Solde après la transaction
    newbalanceOrig = st.number_input(
        "Solde après",
        min_value=0.0,
        value=0.0,
        step=100.0,
        format="%.2f",
        key="new_orig"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SECTION 4 : SOLDES DU COMPTE DESTINATAIRE (celui qui reçoit)
# ============================================================
st.markdown("""
<p style="font-size:11px;color:rgba(255,255,255,0.35);letter-spacing:0.1em;
text-transform:uppercase;font-weight:500;margin-bottom:4px;
font-family:'DM Sans',sans-serif;">📥 Compte destinataire (receveur)</p>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    oldbalanceDest = st.number_input(
        "Solde avant",
        min_value=0.0,
        value=0.0,
        step=100.0,
        format="%.2f",
        key="old_dest"
    )

with col4:
    newbalanceDest = st.number_input(
        "Solde après",
        min_value=0.0,
        value=10000.0,
        step=100.0,
        format="%.2f",
        key="new_dest"
    )

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# ============================================================
# SECTION 5 : BOUTON DE PRÉDICTION
# Quand l'utilisateur clique, on construit le DataFrame et on prédit
# ============================================================
if st.button("🔍  Analyser la transaction"):

    # --- Construction du tableau d'entrée pour le modèle ---
    # Le modèle attend exactement ces colonnes dans cet ordre
    input_data = pd.DataFrame([{
        "type":           clean_type,
        "amount":         amount,
        "oldbalanceOrg":  oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    # --- Prédiction ---
    # model.predict() retourne un tableau → on prend le premier élément [0]
    prediction = model.predict(input_data)[0]

    # --- Probabilité de fraude (si disponible) ---
    # predict_proba retourne [proba_classe_0, proba_classe_1]
    try:
        proba = model.predict_proba(input_data)[0][1]  # Probabilité d'être une fraude
        proba_pct = round(proba * 100, 1)
    except:
        proba_pct = None   # Certains modèles ne supportent pas predict_proba

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================================================
    # AFFICHAGE DU RÉSULTAT
    # On utilise du HTML personnalisé pour un rendu visuel soigné
    # ============================================================

    if prediction == 1:
        # --- CAS FRAUDE DÉTECTÉE ---
        proba_text = f"Indice de confiance : <strong>{proba_pct}%</strong>" if proba_pct else ""
        st.markdown(f"""
        <div style="
            background:rgba(239,68,68,0.08);
            border:1px solid rgba(239,68,68,0.35);
            border-radius:20px; padding:24px 28px;
            animation:fadeUp 0.4s ease;">
            <div style="display:flex; align-items:flex-start; gap:16px;">
                <div style="
                    width:48px; height:48px; border-radius:50%; flex-shrink:0;
                    background:rgba(239,68,68,0.2);
                    display:flex; align-items:center; justify-content:center;
                    font-size:22px;">⚠️</div>
                <div>
                    <div style="
                        font-family:'Playfair Display',serif;
                        font-size:22px; color:#f87171;
                        font-weight:700; margin-bottom:8px;">
                        Transaction Suspecte
                    </div>
                    <p style="
                        color:rgba(255,255,255,0.5); font-size:13px;
                        line-height:1.7; font-family:'DM Sans',sans-serif;">
                        Cette transaction présente des caractéristiques typiques d'une fraude —
                        compte vidé après un transfert ou retrait à haut risque.
                    </p>
                    <div style="
                        margin-top:14px; display:inline-flex; align-items:center; gap:8px;
                        background:rgba(239,68,68,0.15); border-radius:100px;
                        padding:5px 16px; font-family:'DM Mono',monospace;
                        font-size:12px; color:#f87171; font-weight:500;">
                        prédiction = <strong>1 — FRAUDE</strong>
                        {"&nbsp;&nbsp;·&nbsp;&nbsp;" + proba_text if proba_pct else ""}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # --- CAS TRANSACTION LÉGITIME ---
        proba_safe = round((1 - proba) * 100, 1) if proba_pct else None
        proba_text = f"Indice de confiance : <strong>{proba_safe}%</strong>" if proba_safe else ""
        st.markdown(f"""
        <div style="
            background:rgba(16,185,129,0.08);
            border:1px solid rgba(16,185,129,0.3);
            border-radius:20px; padding:24px 28px;">
            <div style="display:flex; align-items:flex-start; gap:16px;">
                <div style="
                    width:48px; height:48px; border-radius:50%; flex-shrink:0;
                    background:rgba(16,185,129,0.2);
                    display:flex; align-items:center; justify-content:center;
                    font-size:22px;">✅</div>
                <div>
                    <div style="
                        font-family:'Playfair Display',serif;
                        font-size:22px; color:#34d399;
                        font-weight:700; margin-bottom:8px;">
                        Transaction Sûre
                    </div>
                    <p style="
                        color:rgba(255,255,255,0.5); font-size:13px;
                        line-height:1.7; font-family:'DM Sans',sans-serif;">
                        Aucun signal de fraude détecté. La transaction semble légitime
                        selon les paramètres analysés par le modèle.
                    </p>
                    <div style="
                        margin-top:14px; display:inline-flex; align-items:center; gap:8px;
                        background:rgba(16,185,129,0.15); border-radius:100px;
                        padding:5px 16px; font-family:'DM Mono',monospace;
                        font-size:12px; color:#34d399; font-weight:500;">
                        prédiction = <strong>0 — LÉGITIME</strong>
                        {"&nbsp;&nbsp;·&nbsp;&nbsp;" + proba_text if proba_safe else ""}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PIED DE PAGE
# ============================================================
st.markdown("""
<br>
<div style="text-align:center;">
    <p style="color:rgba(255,255,255,0.12); font-size:12px; font-family:'DM Mono',monospace;">
        Modèle · LogisticRegression · fraud_detection_pipeline.pkl
    </p>
</div>
""", unsafe_allow_html=True)