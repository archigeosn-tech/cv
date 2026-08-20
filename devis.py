import math
import pandas as pd
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Devis BTP - Terrassement & Fondations",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Application de Chiffrage : Terrassement & Fondations")
st.markdown(
    "Calculez les volumes, quantifiez les matériaux requis (ciment, sable, gravier, fer) et générez un devis global."
)

# Sidebar - Configuration du Projet
st.sidebar.header("📋 Informations du Projet")
nom_projet = st.sidebar.text_input("Nom du projet / Client", "Chantier Villa R+1")
devise = st.sidebar.selectbox("Devise", ["FCFA", "EUR (€)", "USD ($)"], index=0)

# Navigation par onglets
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🚜 1. Terrassement",
        "🧱 2. Dimensionnement Fondations",
        "📊 3. Quantités de Matériaux",
        "💰 4. Devis Global",
    ]
)

# ---------------------------------------------------------
# TAB 1 : TERRASSEMENT
# ---------------------------------------------------------
with tab1:
    st.header("1. Calcul des Terrassements (Déblai / Remblai)")

    col1, col2, col3 = st.columns(3)
    with col1:
        longueur_terr = st.number_input(
            "Longueur d'excavation (m)", min_value=0.0, value=12.0, step=0.5
        )
    with col2:
        largeur_terr = st.number_input(
            "Largeur d'excavation (m)", min_value=0.0, value=10.0, step=0.5
        )
    with col3:
        prof_terr = st.number_input(
            "Profondeur moyenne (m)", min_value=0.0, value=1.2, step=0.1
        )

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        coeff_foisonnement = st.slider(
            "Coefficient de foisonnement",
            min_value=1.0,
            max_value=1.5,
            value=1.25,
            step=0.05,
        )
    with col_f2:
        pu_excavation = st.number_input(
            f"Prix unitaire Excavation ({devise}/m³ en place)",
            min_value=0,
            value=2500,
            step=500,
        )
        pu_evacuation = st.number_input(
            f"Prix unitaire Évacuation ({devise}/m³ foisonné)",
            min_value=0,
            value=3500,
            step=500,
        )

    vol_terr_place = longueur_terr * largeur_terr * prof_terr
    vol_terr_foisonne = vol_terr_place * coeff_foisonnement

    cost_excavation = vol_terr_place * pu_excavation
    cost_evacuation = vol_terr_foisonne * pu_evacuation
    total_terrassement = cost_excavation + cost_evacuation

    m1, m2, m3 = st.columns(3)
    m1.metric("Volume en place", f"{vol_terr_place:.2f} m³")
    m2.metric("Volume foisonné à évacuer", f"{vol_terr_foisonne:.2f} m³")
    m3.metric(
        "Coût Terrassement Total", f"{total_terrassement:,.0f} {devise}"
    )


# ---------------------------------------------------------
# TAB 2 : DIMENSIONNEMENT FONDATIONS
# ---------------------------------------------------------
with tab2:
    st.header("2. Dimensionnement des Éléments de Fondation")

    st.subheader("a) Béton de Propreté")
    col_bp1, col_bp2 = st.columns(2)
    with col_bp1:
        surf_bp = st.number_input(
            "Surface du béton de propreté (m²)",
            min_value=0.0,
            value=100.0,
            step=5.0,
        )
    with col_bp2:
        ep_bp = st.number_input(
            "Épaisseur du béton de propreté (m)",
            min_value=0.01,
            value=0.05,
            step=0.01,
        )
    vol_bp = surf_bp * ep_bp

    st.markdown("---")
    st.subheader("b) Semelles Isolées (Pieds de Poteaux)")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        nb_semelles = st.number_input(
            "Nombre de semelles", min_value=0, value=12, step=1
        )
    with col_s2:
        l_sem = st.number_input(
            "Longueur semelle (m)", min_value=0.0, value=1.2, step=0.1
        )
    with col_s3:
        w_sem = st.number_input(
            "Largeur semelle (m)", min_value=0.0, value=1.2, step=0.1
        )
    with col_s4:
        h_sem = st.number_input(
            "Hauteur/Épaisseur semelle (m)",
            min_value=0.0,
            value=0.4,
            step=0.05,
        )
    vol_semelles_isolees = nb_semelles * (l_sem * w_sem * h_sem)

    st.subheader("c) Semelles Filantes (Rifi / Rigoles)")
    col_sf1, col_sf2, col_sf3 = st.columns(3)
    with col_sf1:
        lin_sem_fil = st.number_input(
            "Mètres linéaires de semelle filante (m)",
            min_value=0.0,
            value=35.0,
            step=1.0,
        )
    with col_sf2:
        w_sem_fil = st.number_input(
            "Largeur semelle filante (m)", min_value=0.0, value=0.5, step=0.05
        )
    with col_sf3:
        h_sem_fil = st.number_input(
            "Hauteur semelle filante (m)", min_value=0.0, value=0.3, step=0.05
        )
    vol_semelles_filantes = lin_sem_fil * w_sem_fil * h_sem_fil

    st.markdown("---")
    st.subheader("d) Amorces de Poteaux (Fut de poteau en sous-sol)")
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        nb_poteaux = st.number_input(
            "Nombre d'amorces poteaux", min_value=0, value=12, step=1
        )
    with col_p2:
        a_pot = st.number_input(
            "Côté A poteau (m)", min_value=0.0, value=0.2, step=0.05
        )
    with col_p3:
        b_pot = st.number_input(
            "Côté B poteau (m)", min_value=0.0, value=0.2, step=0.05
        )
    with col_p4:
        h_pot = st.number_input(
            "Hauteur amorce (m)", min_value=0.0, value=1.0, step=0.1
        )
    vol_poteaux = nb_poteaux * (a_pot * b_pot * h_pot)

    st.markdown("---")
    st.subheader("e) Longrines / Chaînage Bas")
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        lin_longrine = st.number_input(
            "Mètres linéaires de longrines (m)",
            min_value=0.0,
            value=50.0,
            step=1.0,
        )
    with col_l2:
        w_longrine = st.number_input(
            "Largeur longrine (m)", min_value=0.0, value=0.2, step=0.05
        )
    with col_l3:
        h_longrine = st.number_input(
            "Hauteur longrine (m)", min_value=0.0, value=0.3, step=0.05
        )
    vol_longrines = lin_longrine * w_longrine * h_longrine

    st.markdown("---")
    st.subheader("f) Dallage / Hérissonnage (Dalle de forme)")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        surf_dallage = st.number_input(
            "Surface du dallage (m²)", min_value=0.0, value=90.0, step=5.0
        )
    with col_d2:
        ep_dallage = st.number_input(
            "Épaisseur dalle béton (m)", min_value=0.0, value=0.10, step=0.01
        )
    vol_dallage = surf_dallage * ep_dallage

    # Récapitulatif Béton
    vol_beton_arme_total = (
        vol_semelles_isolees
        + vol_semelles_filantes
        + vol_poteaux
        + vol_longrines
        + vol_dallage
    )

    st.success(f"**Volume Béton de Propreté (Non Armé) : {vol_bp:.2f} m³**")
    st.success(
        f"**Volume Béton Armé Total (Semelles, Poteaux, Longrines, Dalle) : {vol_beton_arme_total:.2f} m³**"
    )


# ---------------------------------------------------------
# TAB 3 : QUANTITÉS DE MATÉRIAUX & DOSAGES
# ---------------------------------------------------------
with tab3:
    st.header("3. Dosage du Béton & Calcul des Matériaux Bruts")

    st.sidebar.subheader("⚙️ Paramètres de Dosage")
    dosage_ciment_ba = st.sidebar.number_input(
        "Dosage Ciment Béton Armé (kg/m³)", value=350, step=25
    )
    ratio_acier_ba = st.sidebar.number_input(
        "Ratio Acier/Fer à béton (kg/m³)", value=90, step=5
    )

    # Béton Armé Calculs
    sacs_ciment_ba = math.ceil((vol_beton_arme_total * dosage_ciment_ba) / 50)
    vol_sable_ba = vol_beton_arme_total * 0.40  # env 400L par m3
    vol_gravier_ba = vol_beton_arme_total * 0.80  # env 800L par m3
    poids_acier_kg = vol_beton_arme_total * ratio_acier_ba
    poids_acier_tonnes = poids_acier_kg / 1000

    # Béton Propreté Calculs (dosé à 150-200 kg/m3)
    sacs_ciment_bp = math.ceil((vol_bp * 200) / 50)
    vol_sable_bp = vol_bp * 0.45
    vol_gravier_bp = vol_bp * 0.80

    # Cumul
    total_sacs_ciment = sacs_ciment_ba + sacs_ciment_bp
    total_vol_sable = vol_sable_ba + vol_sable_bp
    total_vol_gravier = vol_gravier_ba + vol_gravier_bp

    st.subheader("📦 Quantités Nécessaires")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Ciment (Sacs de 50kg)", f"{total_sacs_ciment} sacs")
    q2.metric("Sable", f"{total_vol_sable:.2f} m³")
    q3.metric("Gravier (8/16)", f"{total_vol_gravier:.2f} m³")
    q4.metric("Acier / Fer à béton", f"{poids_acier_kg:.0f} kg ({poids_acier_tonnes:.2f} t)")

    st.markdown("---")
    st.subheader("💵 Prix Unitaires des Matériaux")

    pu_col1, pu_col2, pu_col3, pu_col4 = st.columns(4)
    with pu_col1:
        prix_sac_ciment = st.number_input(
            f"Prix 1 Sac de Ciment ({devise})",
            min_value=0,
            value=4500,
            step=100,
        )
    with pu_col2:
        prix_m3_sable = st.number_input(
            f"Prix 1 m³ Sable ({devise})", min_value=0, value=7000, step=500
        )
    with pu_col3:
        prix_m3_gravier = st.number_input(
            f"Prix 1 m³ Gravier ({devise})", min_value=0, value=15000, step=500
        )
    with pu_col4:
        prix_kg_acier = st.number_input(
            f"Prix 1 kg d'Acier ({devise})", min_value=0, value=650, step=25
        )

    # Coûts matériaux
    cost_ciment = total_sacs_ciment * prix_sac_ciment
    cost_sable = total_vol_sable * prix_m3_sable
    cost_gravier = total_vol_gravier * prix_m3_gravier
    cost_acier = poids_acier_kg * prix_kg_acier

    st.subheader("🔨 Main d'œuvre et Coffrage")
    col_mo1, col_mo2 = st.columns(2)
    with col_mo1:
        pu_mo_beton = st.number_input(
            f"Main d'œuvre coulage béton ({devise}/m³)",
            min_value=0,
            value=15000,
            step=1000,
        )
    with col_mo2:
        forfait_coffrage = st.number_input(
            f"Forfait Bois de coffrage & Ferraillage ({devise})",
            min_value=0,
            value=250000,
            step=10000,
        )

    cost_mo = (vol_beton_arme_total + vol_bp) * pu_mo_beton + forfait_coffrage


# ---------------------------------------------------------
# TAB 4 : DEVIS GLOBAL
# ---------------------------------------------------------
with tab4:
    st.header(f"📜 Devis Estimatif - {nom_projet}")

    # Composition du tableau
    items = [
        # Terrassement
        "Terrassement - Excavation / Fouilles",
        "Terrassement - Évacuation des terres",
        # Matériaux Fondations
        "Ciment (Sacs 50kg)",
        "Sable de chantier",
        "Gravier (8/16)",
        "Acier / Fer à béton",
        # Main d'œuvre
        "Main d'œuvre (Coulage + Coffrage + Ferraillage)",
    ]

    quantities = [
        f"{vol_terr_place:.2f} m³",
        f"{vol_terr_foisonne:.2f} m³",
        f"{total_sacs_ciment} sacs",
        f"{total_vol_sable:.2f} m³",
        f"{total_vol_gravier:.2f} m³",
        f"{poids_acier_kg:.0f} kg",
        f"{(vol_beton_arme_total + vol_bp):.2f} m³ (vol. total)",
    ]

    unit_prices = [
        pu_excavation,
        pu_evacuation,
        prix_sac_ciment,
        prix_m3_sable,
        prix_m3_gravier,
        prix_kg_acier,
        pu_mo_beton,
    ]

    totals = [
        cost_excavation,
        cost_evacuation,
        cost_ciment,
        cost_sable,
        cost_gravier,
        cost_acier,
        cost_mo,
    ]

    df_devis = pd.DataFrame(
        {
            "Poste / Désignation": items,
            "Quantité": quantities,
            f"Prix Unitaire ({devise})": [
                f"{p:,.0f}" if isinstance(p, (int, float)) else p
                for p in unit_prices
            ],
            f"Montant Total ({devise})": totals,
        }
    )

    # Affichage du tableau formaté
    df_display = df_devis.copy()
    df_display[f"Montant Total ({devise})"] = df_display[
        f"Montant Total ({devise})"
    ].apply(lambda x: f"{x:,.0f}")
    st.table(df_display)

    grand_total = sum(totals)

    st.subheader(f"🔴 **TOTAL GÉNÉRAL DEVIS : {grand_total:,.0f} {devise}**")

    # Export des données en CSV
    csv = df_devis.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger le devis (CSV)",
        data=csv,
        file_name=f"devis_fondations_{nom_projet.lower().replace(' ', '_')}.csv",
        mime="text/csv",
    )
