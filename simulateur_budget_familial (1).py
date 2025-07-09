
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur Budget Familial", layout="wide")

st.title("📊 Simulateur de Budget Familial Casher")

st.markdown("Utilisez ce simulateur pour estimer votre **reste à vivre mensuel** en fonction de vos revenus, aides et charges.")

# --- Mise en page en deux colonnes ---
left, right = st.columns(2)

# ==== Colonne gauche : Entrée des données ====
with left:
    st.header("🔢 Paramètres")

    st.subheader("👩‍💼 Ton salaire brut")
    salaire_brut = st.slider("Salaire brut mensuel (toi)", 0, 10000, 2200, step=50)
    saisie_salaire_brut = st.number_input("Ou entre le montant brut directement", value=salaire_brut, step=50, key="salaire_input")

    st.subheader("👨‍💼 Salaire brut de ton mari")
    salaire_mari_brut = st.slider("Salaire brut mensuel (mari)", 0, 10000, 2500, step=50)
    saisie_salaire_mari_brut = st.number_input("Ou entre le montant brut de ton mari", value=salaire_mari_brut, step=50, key="mari_input")

    st.subheader("👶 Mode de garde de Maya")
    garde = st.selectbox("Mode de garde", ["Aucun", "Halte-garderie (~50€)", "Crèche (~200€)", "Assistante maternelle (~150€)"])

    st.subheader("🏠 Loyer")
    loyer = st.slider("Montant du loyer", 0, 3000, 1200, step=50)

    st.subheader("📚 Cours particuliers")
    heures_cp = st.slider("Heures de cours particuliers par semaine", 0, 40, 5)
    tarif_cp = st.slider("Tarif horaire (€)", 0, 200, 20, step=5)

# ==== Calculs ====
# Revenu net estimé (brut - 23%)
net = lambda brut: brut * 0.77
salaire_net = net(saisie_salaire_brut)
mari_net = net(saisie_salaire_mari_brut)
revenu_cp = heures_cp * 4.33 * tarif_cp
revenus_total = salaire_net + mari_net + revenu_cp

# Aides sociales estimées
allocation_base = 188
apl = 330
if revenus_total < 2300:
    prime = 300
elif revenus_total < 3000:
    prime = 200
elif revenus_total < 3800:
    prime = 100
else:
    prime = 0
aides = allocation_base + apl + prime

# Mode de garde
if "Halte" in garde:
    garde_cout = 50
elif "Crèche" in garde:
    garde_cout = 200
elif "Assistante" in garde:
    garde_cout = 150
else:
    garde_cout = 0

# Charges fixes estimées
charges = 250
courses = 1500
voiture = 200
telephonie = 50

depenses_total = loyer + garde_cout + charges + courses + voiture + telephonie
reste_a_vivre = revenus_total + aides - depenses_total

# ==== Colonne droite : Résultats ====
with right:
    st.header("📈 Résultats estimés")

    st.metric("Ton revenu net mensuel", f"{salaire_net:,.0f} €")
    st.metric("Revenu net de ton mari", f"{mari_net:,.0f} €")
    st.metric("Aides sociales estimées", f"{aides:,.0f} €")
    st.metric("Total des charges", f"{depenses_total:,.0f} €")
    st.metric("💰 Reste à vivre mensuel", f"{reste_a_vivre:,.0f} €")

# ==== Graphiques ====
st.markdown("---")
st.subheader("📊 Répartition des dépenses")
labels = ["Loyer", "Garde", "Charges", "Courses", "Voiture", "Téléphonie"]
values = [loyer, garde_cout, charges, courses, voiture, telephonie]
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis("equal")
st.pyplot(fig)
