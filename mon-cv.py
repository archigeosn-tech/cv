import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Portfolio | Fallou DIATTA", page_icon="🌊", layout="wide")

# --- STYLE CSS PERSONNALISÉ (Fond Bleu Nuit Dégradé) ---
st.markdown("""
    <style>
    /* Dégradé de bleu de nuit vers bleu ciel */
    .stApp {
        background: linear-gradient(180deg, #001f3f 0%, #0074D9 50%, #7FDBFF 100%);
        color: white;
    }
    
    /* Adaptation des titres pour le fond sombre */
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* Boîtes de contenu semi-transparentes pour la lisibilité */
    .content-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }

    /* Style de la barre latérale */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 31, 63, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Personnalisation des listes */
    .stMarkdown p, .stMarkdown li {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Infos de contact) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📍 Contact</h2>", unsafe_allow_html=True)
    st.image("FD.png", width=150)
    st.write("👤 **Fallou DIATTA**")
    st.write("🏠 Dakar, Sénégal")
    st.write("📧 [archigeosn@gmail.com](mailto:archigeosn@gmail.com)")
    st.write("📞 77 238 99 68")
    st.markdown("---")
    st.info("Disponible pour de nouvelles opportunités en Hydraulique & Géomatique.")

# --- EN-TÊTE ---
st.title("Technicien Supérieur Hydraulicien & Géomaticien")
st.markdown("""
<div class="content-box">
    Expert de la gestion patrimoniale des réseaux hydrauliques, je sécurise la durabilité des infrastructures par le diagnostic de précision, 
    la réhabilitation stratégique et la maîtrise des SIG. Alliant rigueur du béton armé et puissance de l'analyse spatiale, 
    j'optimise l'exploitation et le stockage des ressources en eau.
</div>
""", unsafe_allow_html=True)

# --- FORMATIONS ---
st.header("📚 Parcours Académique")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown("""
    <div class="content-box">
        <strong>ISEP-Thies</strong><br>
        🎓 DTS en Suivi Technique et Gestion des Ouvrages Hydrauliques
    </div>
    """, unsafe_allow_html=True)
with col_f2:
    st.markdown("""
    <div class="content-box">
        <strong>CEDT Le G15</strong><br>
        🎓 BTS en Géomatique
    </div>
    """, unsafe_allow_html=True)

# --- COMPÉTENCES ---
st.header("🛠️ Compétences & Expertises")
c1, c2 = st.columns(2)

with c1:
    with st.container():
        st.subheader("🌐 Géomatique & SIG")
        st.markdown("""
        * ✅ Maîtrise ArcMap & QGIS
        * ✅ Acquisition & Traitement de données
        * ✅ Topographie (Station Totale & Mobil Topo)
        * ✅ Modélisation 2D/3D (AutoCAD & SketchUp)
        * ✅ Outils de travail collaboratifs & Anglais technique
        """)

with c2:
    with st.container():
        st.subheader("💧 Hydraulique & Génie Civil")
        st.markdown("""
        * ✅ Dimensionnement réseaux AEP & Surface libre
        * ✅ Qualité de l'eau & Traitement
        * ✅ Études Géotechniques & Géophysiques
        * ✅ Modélisation DAO (AutoCAD & RSA)
        * ✅ Lecture de plans & Matériaux de construction
        """)

# --- EXPÉRIENCES ---
st.header("🏗️Experiences")
st.markdown("""* 🛠️STAGE EN HYDRAULIQUE
    * Poste : Technicien Superieur en Hydraulique Urbaine / Agricole
    * Entreprise: SOLSO HYDROBAT
    * 📌Thiès""")
st.write(" ▶️Etude reseau AEP")
st.write(" ▶️Dimensionnement reseau AEP")
st.write(" ▶️Gestion des ressources en eau")
st.write(" ▶️Diagnostique des ouvrages")
st.write(" ▶️Reduction des fuites sur un reseau AEP")
st.write(" ▶️Optimisation de la distribution de leau")
st.write(" ▶️Realisation ouvrage de captage: Forage 100m")
