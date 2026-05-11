import streamlit as st
import pandas as pd
from PIL import Image

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Natural Gas Engineering Tool",
    layout="wide"
)

# =========================================================
# LOGO
# =========================================================
try:
    logo = Image.open("suto_logo.png")
    st.image(logo, use_container_width=True)
except:
    st.warning("Logo not found")

# =========================================================
# TITLE
# =========================================================
st.title("Natural Gas Engineering Tool")
st.caption("SUTO iTEC Style Application")

st.markdown("---")

# =========================================================
# GAS INPUT
# =========================================================
st.header("Gas Composition (%)")

col1, col2 = st.columns(2)

with col1:
    ch4 = st.number_input("CH4 (Methane)", value=90.00)
    c2h6 = st.number_input("C2H6 (Ethane)", value=4.72)
    c3h8 = st.number_input("C3H8 (Propane)", value=2.00)
    c4h10 = st.number_input("C4H10 (Butane)", value=0.50)
    n2 = st.number_input("N2 (Nitrogen)", value=1.80)
    co2 = st.number_input("CO2 (Carbon Dioxide)", value=0.70)

with col2:
    c5 = st.number_input("C5H12 (Pentane)", value=0.16)
    c6 = st.number_input("C6H14 (Hexane)", value=0.12)
    c7 = st.number_input("C7H16 (n-Heptane)", value=0.00)
    c8 = st.number_input("C8H18 (3-Methylheptane)", value=0.00)
    h2o = st.number_input("H2O (Water)", value=0.00)
    h2s = st.number_input("H2S (Hydrogen Sulfide)", value=0.00)

# =========================================================
# PROCESS CONDITION
# =========================================================
st.header("Process Condition")

col3, col4 = st.columns(2)

with col3:
    P_bar = st.number_input("Pressure (bar abs)", value=7.0)
    T_C = st.number_input("Temperature (°C)", value=35.0)

with col4:
    Z_manual = st.number_input("Manual Z Override (optional)", value=0.98)

# =========================================================
# UNIT CONVERSION
# =========================================================
P = P_bar * 100000
T = T_C + 273.15

# =========================================================
# GAS PROPERTY TABLE
# =========================================================
st.header("Gas Property Reference")

gas_data = {
    "Component": [
        "CH4","C2H6","C3H8","C4H10",
        "N2","CO2","C5H12","C6H14",
        "C7H16","C8H18","H2O","H2S"
    ],

    "Name": [
        "Methane","Ethane","Propane","Butane",
        "Nitrogen","Carbon Dioxide","Pentane","Hexane",
        "n-Heptane","3-Methylheptane","Water","Hydrogen Sulfide"
    ],

    "M (g/mol)": [
        16,30,44,58,
        28,44,72,86,
        100,114,18,34
    ],

    "Rs (J/kg·K)": [
        518.3,276.5,188.5,143.0,
        296.8,188.9,115.2,96.7,
        83.1,72.9,461.5,244.0
    ],

    "Vol-%": [
        ch4,c2h6,c3h8,c4h10,
        n2,co2,c5,c6,
        c7,c8,h2o,h2s
    ]
}

df = pd.DataFrame(gas_data)

# =========================================================
# CATEGORY
# =========================================================
def category(comp):
    if comp in ["CH4","C2H6"]:
        return "Light Gas"
    elif comp in ["C3H8","C4H10"]:
        return "Medium"
    elif comp.startswith("C") and len(comp) > 3:
        return "Heavy (C5+)"
    elif comp == "N2":
        return "Inert"
    elif comp in ["CO2","H2S"]:
        return "Acid Gas"
    else:
        return "-"

# =========================================================
# PHASE RISK
# =========================================================
def phase_risk(comp):
    if comp in ["C5H12","C6H14","C7H16","C8H18"]:
        return "⚠️ Condensate"
    elif comp == "H2O":
        return "⚠️ Condensate"
    elif comp == "H2S":
        return "☠️ Corrosion Risk"
    else:
        return "Gas"

df["Category"] = df["Component"].apply(category)
df["Phase Risk"] = df["Component"].apply(phase_risk)

# =========================================================
# CONTRIBUTION
# =========================================================
df["M Contribution"] = (
    df["Vol-%"] * df["M (g/mol)"] / 100
)

df["Rs Contribution"] = (
    df["Vol-%"] * df["Rs (J/kg·K)"] / 100
)

# =========================================================
# COLOR STYLE
# =========================================================
def highlight(row):
    if "Heavy" in row["Category"]:
        return ["background-color: #ffcccc"] * len(row)
    elif row["Category"] == "Medium":
        return ["background-color: #fff2cc"] * len(row)
    elif row["Category"] == "Light Gas":
        return ["background-color: #d9ead3"] * len(row)
    else:
        return [""] * len(row)

styled_df = df.style.apply(highlight, axis=1)

st.dataframe(styled_df, use_container_width=True)

# =========================================================
# MIX CALCULATION (SUTO STYLE)
# =========================================================
Mmix = df["M Contribution"].sum()

Rs_mix = 8314 / Mmix

# =========================================================
# NEAR AGA Z
# =========================================================
P_pc = 46
T_pc = 190

P_pr = P_bar / P_pc
T_pr = T / T_pc

Z = 1 - (0.08 * P_pr / T_pr) + (0.015 * (P_pr**2)/(T_pr**2))

Z = max(0.85, min(Z, 1.0))

# manual override
if Z_manual != 0.98:
    Z = Z_manual

# =========================================================
# DENSITY
# =========================================================
rho = P / (Rs_mix * T * Z)

# =========================================================
# RESULT
# =========================================================
st.header("Calculated Mix Property")

col5, col6, col7 = st.columns(3)

with col5:
    st.metric("Mmix (g/mol)", f"{Mmix:.2f}")

with col6:
    st.metric("Rs Mix (J/kg·K)", f"{Rs_mix:.2f}")

with col7:
    st.metric("Density (kg/m³)", f"{rho:.2f}")

st.metric("Z factor (Near-AGA)", f"{Z:.3f}")

# =========================================================
# VALIDATION
# =========================================================
total = (
    ch4+c2h6+c3h8+c4h10+
    n2+co2+c5+c6+
    c7+c8+h2o+h2s
)

if abs(total - 100) > 0.1:
    st.error(f"Total Composition = {total:.2f}% (Must be 100%)")
else:
    st.success("Total Composition Gas OK (100%)")

# =========================================================
# WARNING SYSTEM
# =========================================================
st.header("⚠️ Gas Quality Warning System")

heavy = c5 + c6 + c7 + c8

# Condensate
if heavy > 1:
    st.error("⚠️ HIGH Condensate Risk")
elif heavy > 0.3:
    st.warning("⚠️ Moderate Condensate Risk")
else:
    st.success("✅ Low Condensate Risk")

# CO2
if co2 > 4:
    st.error("⚠️ High CO2")
elif co2 > 2:
    st.warning("⚠️ CO2 Increasing")
else:
    st.success("✅ CO2 Normal")

# H2S
if h2s > 0:
    st.error("☠️ H2S Detected")
else:
    st.success("✅ No H2S detected")

# =========================================================
# OVERALL
# =========================================================
st.header("Overall Assessment")

if heavy > 1 or co2 > 4 or h2s > 0:
    st.error("🚨 GAS CONDITION: ATTENTION REQUIRED")
elif heavy > 0.3 or co2 > 2:
    st.warning("⚠️ GAS CONDITION: MONITORING")
else:
    st.success("✅ GAS CONDITION: STABLE")

# =========================================================
# SMART RECOMMENDATION
# =========================================================
st.header("🧠 Smart Recommendation")

recommendations = []

if heavy > 1:
    recommendations.append("➡️ Check separator / condensate removal")

elif heavy > 0.3:
    recommendations.append("➡️ Monitor condensate trend")

if co2 > 4:
    recommendations.append("➡️ Evaluate CO2 treatment")

elif co2 > 2:
    recommendations.append("➡️ Monitor CO2 trend")

if h2s > 0:
    recommendations.append("➡️ Corrosion inspection recommended")

if len(recommendations) == 0:
    st.success("✅ No action required (Gas condition optimal)")
else:
    for rec in recommendations:
        st.write(rec)

# =========================================================
# NOTES
# =========================================================
st.info("Pressure auto convert bar → Pa")
st.info("Temperature auto convert °C → K")
st.info("Calculation based on SUTO-style gas mix method")
st.info("Near-AGA Z estimation for engineering purpose")
