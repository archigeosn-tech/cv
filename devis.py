import math
import io
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Devis BTP - Terrassement & Fondations",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Application de Chiffrage : Terrassement & Fondations")
st.markdown(
    "Calculez les volumes, quantifiez les matériaux requis (ciment, sable, gravier, fer, briques) et générez un devis global imprimable en PDF."
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
    st.subheader("b) Semelles Isolées (3 Types : S1, S2, S3)")
    
    st.markdown("##### 📌 Semelles Type S1")
    col_s1_1, col_s1_2, col_s1_3, col_s1_4 = st.columns(4)
    with col_s1_1:
        nb_s1 = st.number_input("Nombre de semelles S1", min_value=0, value=6, step=1)
    with col_s1_2:
        l_s1 = st.number_input("Longueur S1 (m)", min_value=0.0, value=1.0, step=0.1)
    with col_s1_3:
        w_s1 = st.number_input("Largeur S1 (m)", min_value=0.0, value=1.0, step=0.1)
    with col_s1_4:
        h_s1 = st.number_input("Hauteur S1 (m)", min_value=0.0, value=0.35, step=0.05)
    vol_s1 = nb_s1 * (l_s1 * w_s1 * h_s1)

    st.markdown("##### 📌 Semelles Type S2")
    col_s2_1, col_s2_2, col_s2_3, col_s2_4 = st.columns(4)
    with col_s2_1:
        nb_s2 = st.number_input("Nombre de semelles S2", min_value=0, value=4, step=1)
    with col_s2_2:
        l_s2 = st.number_input("Longueur S2 (m)", min_value=0.0, value=1.2, step=0.1)
    with col_s2_3:
        w_s2 = st.number_input("Largeur S2 (m)", min_value=0.0, value=1.2, step=0.1)
    with col_s2_4:
        h_s2 = st.number_input("Hauteur S2 (m)", min_value=0.0, value=0.40, step=0.05)
    vol_s2 = nb_s2 * (l_s2 * w_s2 * h_s2)

    st.markdown("##### 📌 Semelles Type S3")
    col_s3_1, col_s3_2, col_s3_3, col_s3_4 = st.columns(4)
    with col_s3_1:
        nb_s3 = st.number_input("Nombre de semelles S3", min_value=0, value=2, step=1)
    with col_s3_2:
        l_s3 = st.number_input("Longueur S3 (m)", min_value=0.0, value=1.5, step=0.1)
    with col_s3_3:
        w_s3 = st.number_input("Largeur S3 (m)", min_value=0.0, value=1.5, step=0.1)
    with col_s3_4:
        h_s3 = st.number_input("Hauteur S3 (m)", min_value=0.0, value=0.45, step=0.05)
    vol_s3 = nb_s3 * (l_s3 * w_s3 * h_s3)

    vol_semelles_isolees = vol_s1 + vol_s2 + vol_s3

    st.markdown("---")
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
    st.subheader("f) Soubassement en Briques Pleines / Agglos Pleins")
    col_br1, col_br2, col_br3 = st.columns(3)
    with col_br1:
        lin_mur_soub = st.number_input(
            "Mètres linéaires de mur de soubassement (m)",
            min_value=0.0,
            value=45.0,
            step=1.0,
        )
    with col_br2:
        h_mur_soub = st.number_input(
            "Hauteur du mur de soubassement (m)",
            min_value=0.0,
            value=0.6,
            step=0.1,
        )
    with col_br3:
        briques_par_m2 = st.number_input(
            "Nombre de briques pleines par m² (ex: 12.5)",
            min_value=1.0,
            value=12.5,
            step=0.5,
        )
    
    surf_mur_soub = lin_mur_soub * h_mur_soub
    nb_briques_raw = surf_mur_soub * briques_par_m2
    nb_briques_total = math.ceil(nb_briques_raw * 1.05)  # 5% de perte

    st.markdown("---")
    st.subheader("g) Dallage / Hérissonnage")
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

    vol_beton_arme_total = (
        vol_semelles_isolees
        + vol_semelles_filantes
        + vol_poteaux
        + vol_longrines
        + vol_dallage
    )

    st.success(f"**Volume Béton de Propreté : {vol_bp:.2f} m³**")
    st.success(
        f"**Volume Béton Armé Total (Semelles, Poteaux, Longrines, Dalle) : {vol_beton_arme_total:.2f} m³**"
    )
    st.info(
        f"**Briques Pleines Soubassement : {nb_briques_total} unités ({surf_mur_soub:.2f} m² avec 5% de perte)**"
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
    ciment_par_brique = st.sidebar.number_input(
        "Ciment mortier pose par brique (kg)", value=1.5, step=0.1
    )

    # Calculs Matériaux
    sacs_ciment_ba = math.ceil((vol_beton_arme_total * dosage_ciment_ba) / 50)
    vol_sable_ba = vol_beton_arme_total * 0.40
    vol_gravier_ba = vol_beton_arme_total * 0.80
    poids_acier_kg = vol_beton_arme_total * ratio_acier_ba
    poids_acier_tonnes = poids_acier_kg / 1000

    sacs_ciment_bp = math.ceil((vol_bp * 200) / 50)
    vol_sable_bp = vol_bp * 0.45
    vol_gravier_bp = vol_bp * 0.80

    sacs_ciment_briques = math.ceil((nb_briques_total * ciment_par_brique) / 50)
    vol_sable_briques = nb_briques_total * 0.003

    total_sacs_ciment = sacs_ciment_ba + sacs_ciment_bp + sacs_ciment_briques
    total_vol_sable = vol_sable_ba + vol_sable_bp + vol_sable_briques
    total_vol_gravier = vol_gravier_ba + vol_gravier_bp

    st.subheader("📦 Quantités Nécessaires")
    q1, q2, q3, q4, q5 = st.columns(5)
    q1.metric("Ciment (Sacs 50kg)", f"{total_sacs_ciment} sacs")
    q2.metric("Sable", f"{total_vol_sable:.2f} m³")
    q3.metric("Gravier (8/16)", f"{total_vol_gravier:.2f} m³")
    q4.metric("Acier / Fer", f"{poids_acier_kg:.0f} kg")
    q5.metric("Briques Pleines", f"{nb_briques_total} u")

    st.markdown("---")
    st.subheader("💵 Prix Unitaires des Matériaux")

    pu_col1, pu_col2, pu_col3, pu_col4, pu_col5 = st.columns(5)
    with pu_col1:
        prix_sac_ciment = st.number_input(f"Prix 1 Sac Ciment ({devise})", min_value=0, value=4500, step=100)
    with pu_col2:
        prix_m3_sable = st.number_input(f"Prix 1 m³ Sable ({devise})", min_value=0, value=7000, step=500)
    with pu_col3:
        prix_m3_gravier = st.number_input(f"Prix 1 m³ Gravier ({devise})", min_value=0, value=15000, step=500)
    with pu_col4:
        prix_kg_acier = st.number_input(f"Prix 1 kg Acier ({devise})", min_value=0, value=650, step=25)
    with pu_col5:
        prix_unitaire_brique = st.number_input(f"Prix 1 Brique ({devise})", min_value=0, value=350, step=25)

    cost_ciment = total_sacs_ciment * prix_sac_ciment
    cost_sable = total_vol_sable * prix_m3_sable
    cost_gravier = total_vol_gravier * prix_m3_gravier
    cost_acier = poids_acier_kg * prix_kg_acier
    cost_briques = nb_briques_total * prix_unitaire_brique

    st.subheader("🔨 Main d'œuvre et Coffrage")
    col_mo1, col_mo2, col_mo3 = st.columns(3)
    with col_mo1:
        pu_mo_beton = st.number_input(f"Main d'œuvre coulage béton ({devise}/m³)", min_value=0, value=15000, step=1000)
    with col_mo2:
        pu_mo_brique = st.number_input(f"Main d'œuvre pose brique ({devise}/unité)", min_value=0, value=100, step=10)
    with col_mo3:
        forfait_coffrage = st.number_input(f"Forfait Bois & Ferraillage ({devise})", min_value=0, value=250000, step=10000)

    cost_mo = (vol_beton_arme_total + vol_bp) * pu_mo_beton + (nb_briques_total * pu_mo_brique) + forfait_coffrage


# ---------------------------------------------------------
# TAB 4 : DEVIS GLOBAL & GENERATION PDF
# ---------------------------------------------------------
def generate_pdf(nom_projet, devise, df_devis, grand_total):
    """Génère un PDF du devis en mémoire à l'aide de ReportLab"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=10,
    )
    subtitle_style = ParagraphStyle(
        "SubTitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=15,
    )
    cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontSize=9,
        leading=11,
    )
    header_cell_style = ParagraphStyle(
        "HeaderCell",
        parent=styles["Normal"],
        fontSize=10,
        leading=12,
        textColor=colors.white,
        fontName="Helvetica-Bold",
    )

    elements = []

    # En-tête
    elements.append(Paragraph("🏗️ DEVIS ESTIMATIF - TERRASSEMENT & FONDATIONS", title_style))
    elements.append(Paragraph(f"<b>Projet / Client :</b> {nom_projet}", subtitle_style))
    elements.append(Paragraph(f"<b>Devise utilisée :</b> {devise}", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=15))

    # Tableau du Devis
    table_data = [[
        Paragraph("Désignation / Poste", header_cell_style),
        Paragraph("Quantité", header_cell_style),
        Paragraph(f"Prix Unitaire ({devise})", header_cell_style),
        Paragraph(f"Montant Total ({devise})", header_cell_style),
    ]]

    for _, row in df_devis.iterrows():
        table_data.append([
            Paragraph(str(row["Poste / Désignation"]), cell_style),
            Paragraph(str(row["Quantité"]), cell_style),
            Paragraph(str(row[f"Prix Unitaire ({devise})"]), cell_style),
            Paragraph(f"{row[f'Montant Total ({devise})']:,.0f}", cell_style),
        ])

    # Total Général
    table_data.append([
        Paragraph("<b>TOTAL GÉNÉRAL DEVIS</b>", cell_style),
        Paragraph("", cell_style),
        Paragraph("", cell_style),
        Paragraph(f"<b>{grand_total:,.0f} {devise}</b>", cell_style),
    ])

    # Style du tableau
    t = Table(table_data, colWidths=[200, 120, 100, 110])
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -2), 0.5, colors.HexColor("#CBD5E0")),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#EDF2F7")),
            ("LINEABOVE", (0, -1), (-1, -1), 1.5, colors.HexColor("#2B6CB0")),
        ])
    )
    elements.append(t)
    
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<i>Devis généré automatiquement par l'application de chiffrage BTP.</i>", cell_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer

with tab4:
    st.header(f"📜 Devis Estimatif - {nom_projet}")

    items = [
        "Terrassement - Excavation / Fouilles",
        "Terrassement - Évacuation des terres",
        "Ciment (Sacs 50kg)",
        "Sable de chantier",
        "Gravier (8/16)",
        "Acier / Fer à béton",
        "Briques Pleines (Soubassement)",
        "Main d'œuvre globale (Coulage + Pose Briques + Coffrage + Ferraillage)",
    ]

    quantities = [
        f"{vol_terr_place:.2f} m³",
        f"{vol_terr_foisonne:.2f} m³",
        f"{total_sacs_ciment} sacs",
        f"{total_vol_sable:.2f} m³",
        f"{total_vol_gravier:.2f} m³",
        f"{poids_acier_kg:.0f} kg",
        f"{nb_briques_total} unités",
        f"Forfait + {(vol_beton_arme_total + vol_bp):.2f}m³ béton + {nb_briques_total} briques",
    ]

    unit_prices = [
        pu_excavation,
        pu_evacuation,
        prix_sac_ciment,
        prix_m3_sable,
        prix_m3_gravier,
        prix_kg_acier,
        prix_unitaire_brique,
        "-",
    ]

    totals = [
        cost_excavation,
        cost_evacuation,
        cost_ciment,
        cost_sable,
        cost_gravier,
        cost_acier,
        cost_briques,
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

    df_display = df_devis.copy()
    df_display[f"Montant Total ({devise})"] = df_display[
        f"Montant Total ({devise})"
    ].apply(lambda x: f"{x:,.0f}")
    st.table(df_display)

    grand_total = sum(totals)

    st.subheader(f"🔴 **TOTAL GÉNÉRAL DEVIS : {grand_total:,.0f} {devise}**")

    st.markdown("---")
    st.subheader("📥 Téléchargements")
    
    col_down1, col_down2 = st.columns(2)
    
    with col_down1:
        # Téléchargement CSV
        csv = df_devis.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📄 Télécharger le devis (CSV / Excel)",
            data=csv,
            file_name=f"devis_fondations_{nom_projet.lower().replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col_down2:
        # Téléchargement PDF
        pdf_bytes = generate_pdf(nom_projet, devise, df_devis, grand_total)
        st.download_button(
            label="📑 Télécharger le devis officiel (PDF)",
            data=pdf_bytes,
            file_name=f"devis_fondations_{nom_projet.lower().replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
