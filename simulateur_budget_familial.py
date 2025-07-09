
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur Budget Familial", layout="centered")

st.title("📊 Simulateur de Budget Familial Casher à Sarcelles")

st.markdown("""Ce simulateur vous permet d'estimer votre **reste à vivre mensuel** en fonction de vos revenus, aides et dépenses fixes.""")

# --- Revenus ---
st.header("👩‍💼 Revenus")
salaire = st.slider("Ton salaire net mensuel (€)", 0, 10000, 1500, step=50)
heures_cp = st.slider("Heures de cours particuliers par semaine", 0, 40, 5)
tarif_cp = st.slider("Tarif horaire des cours particuliers (€)", 0, 1000, 20)
revenu_cp = heures_cp * 4.33 * tarif_cp
mari = st.slider("Salaire net mensuel de ton mari (€)", 0, 10000, 0, step=100)
revenus_total = salaire + revenu_cp + mari

# --- Aides ---
st.header("💶 Aides sociales estimées")
allocation_base = 188
apl = st.slider("APL estimée (€)", 0, 1000, 330)
if revenus_total < 2300:
    prime = 300
elif revenus_total < 3000:
    prime = 200
elif revenus_total < 3800:
    prime = 100
else:
    prime = 0
aides = allocation_base + apl + prime

# --- Dépenses fixes ---
st.header("📦 Dépenses mensuelles")
loyer = st.slider("Loyer (€)", 0, 10000, 1200)
charges = st.slider("Charges (eau, élec, gaz, internet...) (€)", 0, 10000, 250)
courses = st.slider("Courses alimentaires (€)", 0, 10000, 1500)
voiture = st.slider("Frais voiture (€)", 0, 10000, 200)
telephonie = st.slider("Téléphonie + Internet (€)", 0, 10000, 50)

mode_garde = st.selectbox("Mode de garde pour Maya", ["Aucun", "Halte-garderie (~50€)", "Crèche (~200€)", "Assistante maternelle (~150€)"])
if "Halte" in mode_garde:
    garde = 50
elif "Crèche" in mode_garde:
    garde = 200
elif "Assistante" in mode_garde:
    garde = 150
else:
    garde = 0

# --- Dépenses personnalisées ---
st.subheader("➕ Autres postes de dépenses personnalisées")
custom_expenses = {}
nb_custom = st.number_input("Nombre de postes personnalisés à ajouter", min_value=0, max_value=10, value=2)

for i in range(nb_custom):
    label = st.text_input(f"Nom du poste #{i+1}", key=f"label_{i}")
    montant = st.slider(f"Montant pour {label} (€)", 0, 10000, 0, key=f"montant_{i}")
    if label:
        custom_expenses[label] = montant

# --- Dépenses spécifiques (textuelles) ---
st.subheader("🛒 Dépenses détaillées (ex: Carrefour, Picard, etc.)")
depense_detail = st.text_area("Indique ici les catégories de dépenses détaillées ou notes complémentaires")

# --- Calculs ---
depenses_total = loyer + charges + courses + voiture + telephonie + garde + sum(custom_expenses.values())
reste_a_vivre = revenus_total + aides - depenses_total

# --- Résultats ---
st.header("📋 Résumé")
st.metric("Reste à vivre mensuel (€)", f"{reste_a_vivre:,.2f}")

col1, col2 = st.columns(2)
with col1:
    st.metric("Revenus", f"{revenus_total:,.2f} €")
    st.metric("Aides", f"{aides:,.2f} €")
with col2:
    st.metric("Dépenses totales", f"{depenses_total:,.2f} €")
    st.metric("Garde de Maya", f"{garde:,.2f} €")

# --- Graphique ---
st.subheader("📊 Répartition des dépenses")
labels = ["Loyer", "Charges", "Courses", "Voiture", "Téléphonie", "Garde"] + list(custom_expenses.keys())
values = [loyer, charges, courses, voiture, telephonie, garde] + list(custom_expenses.values())
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# --- Notes ---
st.info("Les aides sont estimées : PAJE = 188€, APL = personnalisable, Prime d'activité variable selon le revenu du foyer.")
if depense_detail:
    st.markdown("### 📝 Notes complémentaires :")
    st.markdown(depense_detail)
