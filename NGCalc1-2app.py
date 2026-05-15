from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# =========================================================
# NATURAL GAS ENGINEERING TOOL
# SUTO STYLE ENGINE + ERROR ANALYSIS
# =========================================================

import time
import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime


# =========================================================
# LOGO
# =========================================================
try:
    logo = Image.open("suto_logo.png")
    st.image(logo, use_container_width=True)
except:
    st.warning("Logo not found")

language = st.sidebar.selectbox(
    "Language",
    ["English", "Indonesia"]
)

# =========================================================
# TRANSLATION
# =========================================================

if language == "English":

    TXT_TITLE = "Natural Gas Engineering Suite"
    TXT_GASCOMP = "Gas Composition"
    TXT_PROCESS = "Process Conditions"
    TXT_RESULT = "Calculated Properties"
    TXT_WARNING = "Gas Quality Warning"
    TXT_RECOMMEND = "Engineering Recommendation"

else:

    TXT_TITLE = "Suite Engineering Gas Alam"
    TXT_GASCOMP = "Komposisi Gas"
    TXT_PROCESS = "Kondisi Proses"
    TXT_RESULT = "Hasil Perhitungan"
    TXT_WARNING = "Peringatan Kualitas Gas"
    TXT_RECOMMEND = "Rekomendasi Engineering"


# =========================================================
# PAGE CONFIG
# =========================================================


st.set_page_config(
    page_title="CW GAS ENGINEER",
    layout="wide"
)

# =========================================================
# SPLASH SCREEN
# =========================================================

splash = st.empty()

splash.markdown(
    """
    <style>
    .splash-container {
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        height:70vh;
        color:white;
    }

    .splash-title {
        font-size:60px;
        font-weight:bold;
        color:#00b388;
    }

    .splash-sub {
        font-size:24px;
        color:#ffe000;
    }
    </style>

    <div class="splash-container">
        <div class="splash-title">CW</div>
        <div class="splash-sub">SUTO GAS ENGINEER</div>
    </div>
    """,
    unsafe_allow_html=True
)

time.sleep(2)

splash.empty()

# =========================================================
# LOADING SPINNER
# =========================================================

with st.spinner(
    "Loading CW Gas Engineer Suite..."
):
    time.sleep(1.5)


# =========================================================
# MAIN DASHBOARD
# =========================================================

st.title("CW GAS ENGINEER")


# =========================================================
# TITLE
# =========================================================
st.title("Natural Gas Engineering Tool")
st.caption("SUTO iTEC Style Application")

st.markdown("---")

# =========================================================
# GAS INPUT
# =========================================================
st.header(TXT_GASCOMP)

col1, col2 = st.columns(2)

with col1:

    ch4 = st.number_input(
        "CH4 (Methane)",
        value=90.00
    )

    c2h6 = st.number_input(
        "C2H6 (Ethane)",
        value=4.72
    )

    c3h8 = st.number_input(
        "C3H8 (Propane)",
        value=2.00
    )

    c4h10 = st.number_input(
        "C4H10 (Butane)",
        value=0.50
    )

    n2 = st.number_input(
        "N2 (Nitrogen)",
        value=1.80
    )

    co2 = st.number_input(
        "CO2 (Carbon Dioxide)",
        value=0.70
    )

with col2:

    c5 = st.number_input(
        "C5H12 (Pentane)",
        value=0.16
    )

    c6 = st.number_input(
        "C6H14 (Hexane)",
        value=0.12
    )

    c7 = st.number_input(
        "C7H16 (n-Heptane)",
        value=0.00
    )

    c8 = st.number_input(
        "C8H18 (3-Methylheptane)",
        value=0.00
    )

    h2o = st.number_input(
        "H2O (Water)",
        value=0.00
    )

    h2s = st.number_input(
        "H2S (Hydrogen Sulfide)",
        value=0.00
    )

# =========================================================
# PROCESS CONDITION
# =========================================================

st.header("Process Condition")

col3, col4 = st.columns(2)

with col3:

    P_bar = st.number_input(
        "Pressure (bar abs)",
        value=7.0
    )

    T_C = st.number_input(
        "Temperature (°C)",
        value=35.0
    )

with col4:

    Z_manual = st.number_input(
        "Manual Z Override",
        value=0.98
    )

# =========================================================
# UNIT CONVERSION
# =========================================================
P = P_bar * 100000
T = T_C + 273.15

# =========================================================
# GAS PROPERTY DATABASE
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

    if comp in [
        "C5H12","C6H14",
        "C7H16","C8H18"
    ]:
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

styled_df = df.style.apply(
    highlight,
    axis=1
)

st.dataframe(
    styled_df,
    use_container_width=True
)

# =========================================================
# MIX CALCULATION
# =========================================================
Mmix = df["M Contribution"].sum()

Rs_mix = 8314 / Mmix

# =========================================================
# NEAR AGA Z FACTOR
# =========================================================
P_pc = 46
T_pc = 190

P_pr = P_bar / P_pc
T_pr = T / T_pc

Z = (
    1
    - (0.08 * P_pr / T_pr)
    + (0.015 * (P_pr**2)/(T_pr**2))
)

Z = max(0.85, min(Z, 1.0))

# Manual override
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

    st.metric(
        "Mmix (g/mol)",
        f"{Mmix:.2f}"
    )

with col6:

    st.metric(
        "Rs Mix (J/kg·K)",
        f"{Rs_mix:.2f}"
    )

with col7:

    st.metric(
        "Density (kg/m³)",
        f"{rho:.2f}"
    )

st.metric(
    "Z factor (Near-AGA)",
    f"{Z:.3f}"
)

# =========================================================
# ERROR ANALYSIS
# =========================================================
st.header("Error Analysis")

# FLOW ERROR
actual = st.number_input(
    "Actual Flow (reference)",
    value=100.0
)

measured = st.number_input(
    "Measured Flow (S401)",
    value=100.0
)

flow_error = (
    (measured - actual) / actual
) * 100

st.metric(
    "Flow Error (%)",
    f"{flow_error:.2f}"
)

if flow_error > 0:

    st.warning(
        "⚠️ OVER-reading → S401 reading HIGHER than actual"
    )

elif flow_error < 0:

    st.warning(
        "⚠️ UNDER-reading → S401 reading LOWER than actual"
    )

else:

    st.success(
        "✅ Flow reading matched"
    )

# Rs ERROR
st.subheader("Gas Constant (Rs) Error")

R_actual = Rs_mix

R_setting = st.number_input(
    "Rs setting di S401",
    value=370.0
)

error_rs = (
    (R_actual / R_setting) - 1
) * 100

st.metric(
    "Error akibat Rs (%)",
    f"{error_rs:.2f}"
)

# =========================================================
# FLOW READING SIMULATION
# =========================================================

st.subheader("Flow Reading Simulation")

simulated_flow = (
    actual *
    (R_actual / R_setting)
)

st.metric(
    "Simulated S401 Reading",
    f"{simulated_flow:.2f}"
)

difference_flow = (
    simulated_flow - actual
)

st.metric(
    "Flow Difference",
    f"{difference_flow:.2f}"
)

# Interpretation
if simulated_flow > actual:

    st.warning(
        f"""
        ⚠️ S401 Potential overreading approximately 
        {difference_flow:.2f}

        (OVER-reading)
        """
    )

elif simulated_flow < actual:

    st.warning(
        f"""
        ⚠️ S401 Potential under-reading approximately 
        {abs(difference_flow):.2f}

        (UNDER-reading)
        """
    )

else:

    st.success(
        "✅ Simulated reading matched actual flow"
    )

if error_rs > 0:

    st.warning(
        "⚠️ Rs setting to small → S401 potential OVER-reading"
    )

    st.info(
        f"""
        Actual Rs = {R_actual:.2f} J/kg·K

        S401 Rs = {R_setting:.2f} J/kg·K

        Because the Rs setting is lower, 
        the thermal mass flowmeter will read 
        flow higher than actual.
        """
    )

elif error_rs < 0:

    st.warning(
        "⚠️ Rs setting is to high → S401 potential UNDER-reading"
    )

    st.info(
        f"""
        Actual Rs = {R_actual:.2f} J/kg·K

        S401 Rs = {R_setting:.2f} J/kg·K

        Because the Rs setting is higher, 
        the thermal mass flowmeter will read 
        flow lower than actual.
        """
    )

else:

    st.success(
        "✅ Rs setting are correct"
    )

# =========================================================
# ENGINEERING RECOMMENDATION
# =========================================================
st.subheader("Engineering Recommendation")

if abs(error_rs) > 5:

    st.error(
        "🚨 Rs mismatch besar → recalibration recommended"
    )

elif abs(error_rs) > 2:

    st.warning(
        "⚠️ Rs mismatch moderat → monitor measurement accuracy"
    )

else:

    st.success(
        "✅ Rs mismatch acceptable"
    )

# =========================================================
# VALIDATION
# =========================================================

st.header("Gas Composition Validation")

total = (
    ch4 + c2h6 + c3h8 + c4h10 +
    n2 + co2 + c5 + c6 +
    c7 + c8 + h2o + h2s
)

# Display total
st.metric(
    "Total Gas Composition (%)",
    f"{total:.2f}"
)

difference = abs(100 - total)

st.caption("Custom for Others Gas")
st.caption("Nm3/h use reference temperature : 15 DegC")
st.caption("Sm3/h use reference temperature : 20 DegC")
st.caption("Reference pressure (hPa) : 1013.2")

# =========================================================
# VALIDATION LOGIC
# =========================================================

if difference < 0.01:

    st.success(
        """
        ✅ Total Composition Gas OK (100%)

        Gas composition is appropriate 
        and valid for calculation.
        """
    )

elif difference < 1:

    st.warning(
        f"""
        ⚠️ Total composition slightly off

        Current total = {total:.2f}%

        Difference = {difference:.2f}%

        It is better to double check the input gas composition.
        """
    )

else:

    st.error(
        f"""
        🚨 Total gas composition invalid

        Current total = {total:.2f}%

        Difference = {difference:.2f}%

        Calculation may be inaccurate.
        """
    )
# =========================================================
# WARNING SYSTEM
# =========================================================
st.header("⚠️ Gas Quality Warning System")

heavy = c5 + c6 + c7 + c8

# Condensate
if heavy > 1:

    st.error(
        "⚠️ HIGH Condensate Risk"
    )

elif heavy > 0.3:

    st.warning(
        "⚠️ Moderate Condensate Risk"
    )

else:

    st.success(
        "✅ Low Condensate Risk"
    )

# CO2
if co2 > 4:

    st.error(
        "⚠️ High CO2"
    )

elif co2 > 2:

    st.warning(
        "⚠️ CO2 Increasing"
    )

else:

    st.success(
        "✅ CO2 Normal"
    )

# H2S
if h2s > 0:

    st.error(
        "☠️ H2S Detected"
    )

else:

    st.success(
        "✅ No H2S detected"
    )

# =========================================================
# OVERALL ASSESSMENT
# =========================================================
st.header("Overall Assessment")

if heavy > 1 or co2 > 4 or h2s > 0:

    st.error(
        "🚨 GAS CONDITION: ATTENTION REQUIRED"
    )

elif heavy > 0.3 or co2 > 2:

    st.warning(
        "⚠️ GAS CONDITION: MONITORING"
    )

else:

    st.success(
        "✅ GAS CONDITION: STABLE"
    )

# =========================================================
# SMART RECOMMENDATION
# =========================================================
st.header("🧠 Smart Recommendation")

recommendations = []

if heavy > 1:
    recommendations.append(
        "➡️ Check separator / condensate removal"
    )

elif heavy > 0.3:
    recommendations.append(
        "➡️ Monitor condensate trend"
    )

if co2 > 4:
    recommendations.append(
        "➡️ Evaluate CO2 treatment"
    )

elif co2 > 2:
    recommendations.append(
        "➡️ Monitor CO2 trend"
    )

if h2s > 0:
    recommendations.append(
        "➡️ Corrosion inspection recommended"
    )

if len(recommendations) == 0:

    st.success(
        "✅ No action required (Gas condition optimal)"
    )

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

# =========================================================
# REPORT INFORMATION
# =========================================================

st.header("Report Information")

customer_name = st.text_input(
    "Customer Name",
    value="Client Name"
)

project_name = st.text_input(
    "Project / Site",
    value="Natural Gas System"
)

# =========================================================
# PDF REPORT
# =========================================================

def generate_pdf():

    doc = SimpleDocTemplate(
        "Gas_Report.pdf"
    )

    styles = getSampleStyleSheet()

    elements = []

    # =====================================================
    # DATE
    # =====================================================

    report_date = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    # =====================================================
    # TITLE
    # =====================================================

    title = Paragraph(
        "CW GAS ENGINEER REPORT",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # =====================================================
    # CUSTOMER INFO
    # =====================================================

    info_data = [

        ["Customer", customer_name],

        ["Project", project_name],

        ["Date", report_date]

    ]

    info_table = Table(info_data)

    info_table.setStyle(TableStyle([

        ('GRID', (0,0), (-1,-1), 1, colors.grey),

        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),

        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold')

    ]))

    elements.append(info_table)

    elements.append(Spacer(1, 20))

    # =====================================================
    # GAS COMPOSITION TABLE
    # =====================================================

    gas_table_data = [

        ["Component", "Vol %"]

    ]

    for i in range(len(df)):

        gas_table_data.append([

            df.iloc[i]["Component"],

            f"{df.iloc[i]['Vol-%']:.2f}"

        ])

    gas_table = Table(gas_table_data)

    gas_table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.black),

        ('TEXTCOLOR', (0,0), (-1,0), colors.yellow),

        ('GRID', (0,0), (-1,-1), 1, colors.grey),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')

    ]))

    elements.append(
        Paragraph(
            "Gas Composition",
            styles['Heading2']
        )
    )

    elements.append(gas_table)

    elements.append(Spacer(1, 20))

    # =====================================================
    # CALCULATED PROPERTY
    # =====================================================

    calc_data = [

        ["Parameter", "Value"],

        ["Molecular Weight", f"{Mmix:.2f} g/mol"],

        ["Gas Constant", f"{Rs_mix:.2f} J/kg.K"],

        ["Density", f"{rho:.2f} kg/m3"],

        ["Z Factor", f"{Z:.3f}"],

        ["Pressure", f"{P_bar:.2f} barA"],

        ["Temperature", f"{T_C:.2f} °C"]

    ]

calc_table = Table(calc_data)

    calc_table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.black),

        ('TEXTCOLOR', (0,0), (-1,0), colors.yellow),

        ('GRID', (0,0), (-1,-1), 1, colors.grey),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke)

    ]))
    elements.append(
        Paragraph(
            "Calculated Properties",
            styles['Heading2']
        )
    )

    elements.append(calc_table)

    elements.append(Spacer(1, 20))

    # =====================================================
    # ENGINEERING NOTE
    # =====================================================

    note = Paragraph(
        """
        Engineering assessment generated automatically
        by CW GAS ENGINEER.
        """,
        styles['BodyText']
    )

    elements.append(note)

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(elements)

# =========================================================
# EXPORT REPORT
# =========================================================

st.header("Export Report")

if st.button(
    "Generate PDF Report",
    key="pdf_button"
):

    generate_pdf()

    with open(
        "Gas_Report.pdf",
        "rb"
    ) as pdf_file:

        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="Gas_Report.pdf",
            mime="application/pdf",
            key="download_pdf"
        )

    # =====================================================
    # TITLE
    # =====================================================

    title = Paragraph(
        "CW GAS ENGINEER REPORT",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    # =====================================================
    # CUSTOMER INFO
    # =====================================================

    info_data = [

        ["Customer", customer_name],

        ["Project", project_name],

        ["Date", report_date]

    ]

    info_table = Table(info_data)

    info_table.setStyle(TableStyle([

        ('GRID', (0,0), (-1,-1), 1, colors.grey),

        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),

        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold')

    ]))

    elements.append(info_table)

    elements.append(Spacer(1, 20))

    # =====================================================
    # GAS COMPOSITION
    # =====================================================

    gas_table_data = [

        ["Component", "Vol %"]

    ]

    for i in range(len(df)):

        gas_table_data.append([

            df.iloc[i]["Component"],

            f"{df.iloc[i]['Vol-%']:.2f}"

        ])

    gas_table = Table(gas_table_data)

    gas_table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.black),

        ('TEXTCOLOR', (0,0), (-1,0), colors.yellow),

        ('GRID', (0,0), (-1,-1), 1, colors.grey),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')

    ]))

    elements.append(
        Paragraph(
            "Gas Composition",
            styles['Heading2']
        )
    )

    elements.append(gas_table)

    elements.append(Spacer(1, 20))

# =====================================================
# GAS COMPOSITION TABLE
# =====================================================

gas_table_data = [

    ["Component", "Vol %"]

]

for i in range(len(df)):

    gas_table_data.append([

        df.iloc[i]["Component"],

        f"{df.iloc[i]['Vol-%']:.2f}"

    ])

gas_table = Table(gas_table_data)

gas_table.setStyle(TableStyle([

    ('BACKGROUND', (0,0), (-1,0), colors.black),

    ('TEXTCOLOR', (0,0), (-1,0), colors.yellow),

    ('GRID', (0,0), (-1,-1), 1, colors.grey),

    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')

]))

elements.append(
    Paragraph(
        "Gas Composition",
        styles['Heading2']
    )
)

elements.append(gas_table)

elements.append(Spacer(1, 20))
    
# =====================================================
# CALCULATED PROPERTY
# =====================================================

calc_data = [

    ["Parameter", "Value"],
    
    ["Molecular Weight", f"{Mmix:.2f} g/mol"],
    
    ["Gas Constant", f"{Rs_mix:.2f} J/kg.K"],
    
    ["Density", f"{rho:.2f} kg/m3"],
    
    ["Z Factor", f"{Z:.3f}"],
    
    ["Pressure", f"{P_bar:.2f} barA"],
    
    ["Temperature", f"{T_C:.2f} °C"]
    
]

    calc_table = Table(calc_data)

    calc_table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.black),

        ('TEXTCOLOR', (0,0), (-1,0), colors.yellow),

        ('GRID', (0,0), (-1,-1), 1, colors.grey),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke)

    ]))

    elements.append(
        Paragraph(
            "Calculated Properties",
            styles['Heading2']
        )
    )

    elements.append(calc_table)

    elements.append(Spacer(1, 20))

    # =====================================================
    # ENGINEERING NOTE
    # =====================================================

    note = Paragraph(
        """
        Engineering report generated automatically
        by CW GAS ENGINEER.
        """,
        styles['BodyText']
    )

    elements.append(note)

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(elements)
    # =====================================================
    # SUMMARY TABLE
    # =====================================================

    data = [

        ["Parameter", "Value"],

        ["Molecular Weight", f"{Mmix:.2f} g/mol"],

        ["Gas Constant", f"{Rs_mix:.2f} J/kg.K"],

        ["Density", f"{rho:.2f} kg/m3"],

        ["Z Factor", f"{Z:.3f}"],

        ["Pressure", f"{P_bar:.2f} barA"],

        ["Temperature", f"{T_C:.2f} °C"]

    ]

    table = Table(data)

    table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.black),

        ('TEXTCOLOR', (0,0), (-1,0), colors.yellow),

        ('GRID', (0,0), (-1,-1), 1, colors.grey),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke)

    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    rec = Paragraph(
        """
        Engineering assessment generated automatically
        by CW GAS ENGINEER.
        """,
        styles['BodyText']
    )

    elements.append(rec)

    doc.build(elements)

# =========================================================
# REPORT INFORMATION
# =========================================================

st.header("Report Information")

customer_name = st.text_input(
    "Customer Name",
    value="Client Name"
)

project_name = st.text_input(
    "Project / Site",
    value="Natural Gas System"
)

# =========================================================
# EXPORT REPORT
# =========================================================

st.header("Export Report")

if st.button("Generate PDF Report"):

    generate_pdf()

    with open(
        "Gas_Report.pdf",
        "rb"
    ) as pdf_file:

        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="Gas_Report.pdf",
            mime="application/pdf"
        )
