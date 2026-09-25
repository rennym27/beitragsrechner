import streamlit as st

st.set_page_config(page_title="TCME Beitragsrechner 2027", layout="wide")

st.title("🎾 TCME Mitgliedsbeiträge & Beitragsrechner 2027")
st.markdown("Passen Sie die **variablen Parameter** in der linken Seitenleiste an, um die Auswirkungen auf die Einnahmen direkt zu berechnen.")

# ==========================================
# SEITENLEISTE: VARIABLE PARAMETER (Orange)
# ==========================================
st.sidebar.header("⚙️ Variable Parameter 2027")

st.sidebar.subheader("1. Beitragssätze 2027 (€)")
b_em = st.sidebar.number_input("Einzelmitgliedschaft", value=150, step=5)
b_epm = st.sidebar.number_input("Ehepaare", value=250, step=5)
b_vm = st.sidebar.number_input("Verkehrsmitglieder", value=75, step=5)
b_jm = st.sidebar.number_input("Jugendliche (15-18 J.)", value=70, step=5)
b_km = st.sidebar.number_input("Kinder (bis 14 J.)", value=35, step=5)
b_pm = st.sidebar.number_input("Passivmitglieder", value=25, step=5)

st.sidebar.subheader("2. Familientarife 2027 (€)")
b_fm_2e = st.sidebar.number_input("Familienbeitrag (2 E + K)", value=280, step=5)
b_fm_1e = st.sidebar.number_input("Familienbeitrag (1 E + K)", value=180, step=5)

st.sidebar.subheader("3. Arbeitsdienst Parameter")
ad_stunden = st.sidebar.number_input("Stunden pro Mitglied (18-70 J.)", value=3.0, step=0.5)
ad_kosten = st.sidebar.number_input("Kosten pro Stunde (€)", value=10.0, step=1.0)
ad_erfuellung = st.sidebar.slider("Erfüllungsquote (%)", min_value=0, max_value=100, value=70, step=5) / 100.0

st.sidebar.subheader("4. Mitgliederzahlen")
n_erwachsene = st.sidebar.number_input("Erwachsene gesamt", value=66)
n_ehepaare = st.sidebar.number_input("Ehepaare gesamt", value=33)
n_vm = st.sidebar.number_input("Verkehrsmitglieder", value=9)
n_jm = st.sidebar.number_input("Jugendliche", value=16)
n_km = st.sidebar.number_input("Kinder", value=52)
n_pm = st.sidebar.number_input("Passivmitglieder", value=26)
n_ehren = st.sidebar.number_input("Ehrenmitglieder", value=3)

st.sidebar.subheader("5. davon in Familientarif")
n_fm_2e = st.sidebar.number_input("Familien mit 2 E", value=7)
n_fm_1e = st.sidebar.number_input("Familien mit 1 E", value=12)

# ==========================================
# BERECHNUNGEN (entsprechend Excel-Formeln)
# ==========================================

# Festwerte 2026 für Vergleich
b2026_em, b2026_epm, b2026_vm, b2026_jm, b2026_km, b2026_pm = 150, 250, 75, 70, 35, 25
einnahmen_2026 = (n_erwachsene * b2026_em + 
                  (n_ehepaare / 2) * b2026_epm + 
                  n_vm * b2026_vm + 
                  n_jm * b2026_jm + 
                  n_km * b2026_km + 
                  n_pm * b2026_pm)

# Betroffene Personen in Familientarifen
fm_erwachsene = n_fm_2e * 2 + n_fm_1e
fm_ehepaare = n_fm_2e * 2
fm_vm = 0  # laut Matrix
fm_jm = 8  # laut Matrix aus Excel Tabelle2
fm_km = 14 # laut Matrix aus Excel Tabelle2

# Reguläre Zahler (ohne Familientarif)
reg_erwachsene = n_erwachsene - fm_erwachsene
reg_ehepaare = n_ehepaare - fm_ehepaare
reg_vm = n_vm - fm_vm
reg_jm = n_jm - fm_jm
reg_km = n_km - fm_km
reg_pm = n_pm

# Einnahmen 2027
einnahmen_regulaer = (reg_erwachsene * b_em + 
                     (reg_ehepaare / 2) * b_epm + 
                     reg_vm * b_vm + 
                     reg_jm * b_jm + 
                     reg_km * b_km + 
                     reg_pm * b_pm)

einnahmen_familien = (n_fm_2e * b_fm_2e) + (n_fm_1e * b_fm_1e)
einnahmen_2027 = einnahmen_regulaer + einnahmen_familien

# Arbeitsdienst
# Berechtigte Mitglieder (Erwachsene + Ehepaare + Verkehrsmitglieder)
arbeitsdienst_pflichtige = n_erwachsene + n_ehepaare + n_vm
einnahmen_arbeitsdienst = arbeitsdienst_pflichtige * ad_stunden * ad_kosten * (1 - ad_erfuellung)
einnahmen_gesamt_2027 = einnahmen_2027 + einnahmen_arbeitsdienst

# ==========================================
# HAUPTSEITE: ERGEBNISSE & ANANLYSE
# ==========================================

col1, col2, col3 = st.columns(3)
col1.metric("Beiträge 2026", f"{einnahmen_2026:,.2f} €")
col2.metric("Beiträge 2027 (ohne AD)", f"{einnahmen_2027:,.2f} €", delta=f"{einnahmen_2027 - einnahmen_2026:,.2f} €")
col3.metric("Gesamteinnahmen 2027 (inkl. AD)", f"{einnahmen_gesamt_2027:,.2f} €")

st.markdown("---")

st.subheader("📊 Detailübersicht Arbeitsdienst")
ad_col1, ad_col2, ad_col3 = st.columns(3)
ad_col1.write(f"**Arbeitspflichtige Mitglieder:** {arbeitsdienst_pflichtige}")
ad_col2.write(f"**Soll-Stunden gesamt:** {arbeitsdienst_pflichtige * ad_stunden:.0f} Std.")
ad_col3.write(f"**Erwartete Einnahmen (Ablöse):** {einnahmen_arbeitsdienst:,.2f} €")

st.markdown("---")

st.subheader("💡 Kostenvergleich für Familien")
st.markdown("Vergleich derregulären Einzelbeiträge im Vergleich zum neuen Familienbeitrag:")

v_col1, v_col2, v_col3, v_col4 = st.columns(4)

with v_col1:
    einzel_2e_1j = b_epm + b_jm
    diff_2e_1j = b_fm_2e - einzel_2e_1j
    st.markdown("**2 E + 1 J**")
    st.write(f"Einzel: {einzel_2e_1j} €")
    st.write(f"Familie: {b_fm_2e} €")
    st.write(f"**Differenz: {diff_2e_1j} €**")

with v_col2:
    einzel_2e_1k = b_epm + b_km
    diff_2e_1k = b_fm_2e - einzel_2e_1k
    st.markdown("**2 E + 1 K**")
    st.write(f"Einzel: {einzel_2e_1k} €")
    st.write(f"Familie: {b_fm_2e} €")
    st.write(f"**Differenz: {diff_2e_1k} €**")

with v_col3:
    einzel_1e_1j = b_em + b_jm
    diff_1e_1j = b_fm_1e - einzel_1e_1j
    st.markdown("**1 E + 1 J**")
    st.write(f"Einzel: {einzel_1e_1j} €")
    st.write(f"Familie: {b_fm_1e} €")
    st.write(f"**Differenz: {diff_1e_1j} €**")

with v_col4:
    einzel_1e_1k = b_em + b_km
    diff_1e_1k = b_fm_1e - einzel_1e_1k
    st.markdown("**1 E + 1 K**")
    st.write(f"Einzel: {einzel_1e_1k} €")
    st.write(f"Familie: {b_fm_1e} €")
    st.write(f"**Differenz: {diff_1e_1k} €**")
