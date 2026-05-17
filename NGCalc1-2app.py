# =========================================================
# CW GAS ENGINEER
# FULL CLEAN VERSION
# =========================================================

import time
import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime

# PDF
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
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CW GAS ENGINEER",
    layout="wide"
)

# =========================================================
# LOGO
# =========================================================

try:
    logo = Image.open("suto_logo.png")
    st.image(logo, width=250)
except:
    st.warning("Logo not found")

# =========================================================
# SPLASH
# =========================================================

splash = st.empty()

splash.markdown(
    """
    <div style='text-align:center;padding-top:150px;'>
        <h1 style='color:#00b388;font-size:60px;'>
            CW GAS ENGINEER
        </h1>

        <h3 style='color:#ffe000;'>
            SUTO Engineering Suite
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

time.sleep(1.5)

splash.empty()

# =========================================================
# TITLE
# =========================================================

st.title("Natural Gas Engineering Tool")
st.caption("SUTO iTEC Style")

st.markdown("---")

# =========================================================
# CUSTOMER INFO
# =========================================================

st.header("Customer Information")

colA, colB = st.columns(2)

with colA:

    customer_name = st.text_input(
        "Customer Name",
        value="Customer"
    )

with colB:

    project_name = st.text_input(
        "Project Name",
        value="Natural Gas System"
    )

# =========================================================
# GAS INPUT
# =========================================================

st.header("Gas Composition")

col1, col2 = st.columns(2)

with col1:

    ch4 = st.number_input("CH4 (%)", value=90.00)
    c2h6 = st.number_input("C2H6 (%)", value=4.72)
    c3h8 = st.number_input("C3H8 (%)", value=2.00)
    c4h10 = st.number_input("C4H10 (%)", value=0.50)
    n2 = st.number_input("N2 (%)", value=1.80)
    co2 = st.number_input("CO2 (%)", value=0.70)

with col2:

    c5 = st.number_input("C5H12 (%)", value=0.16)
    c6 = st.number_input("C6H14 (%)", value=0.12)
    c7 = st.number_input("C7H16 (%)", value=0.00)
    c8 = st.number_input("C8H18 (%)", value=0.00)
    h2o = st.number_input("H2O (%)", value=0.00)
    h2s = st.number_input("H2S (%)", value=0.00)

# =========================================================
# PROCESS CONDITION
# =========================================================

st.header("Process Condition")

col3, col4 = st.columns(2)

with col3:

    P_bar = st.number_input(
        "Pressure (barA)",
        value=7.0
    )

with col4:

    T_C = st.number_input(
        "Temperature (°C)",
        value=35.0
    )

# =========================================================
# CALCULATION
# =========================================================

gas_data = {

    "Component": [
        "CH4","C2H6","C3H8","C4H10",
        "N2","CO2","C5H12","C6H14",
        "C7H16","C8H18","H2O","H2S"
    ],

    "Vol-%": [
        ch4,c2h6,c3h8,c4h10,
        n2,co2,c5,c6,
        c7,c8,h2o,h2s
    ],

    "MW": [
        16,30,44,58,
        28,44,72,86,
        100,114,18,34
    ]
}

df = pd.DataFrame(gas_data)

df["Contribution"] = (
    df["Vol-%"] * df["MW"] / 100
)

Mmix = df["Contribution"].sum()

Rs_mix = 8314 / Mmix

P = P_bar * 100000
T = T_C + 273.15

Z = 0.98

rho = P / (Rs_mix * T * Z)

# =========================================================
# RESULT
# =========================================================

st.header("Calculated Properties")

col5, col6, col7 = st.columns(3)

with col5:

    st.metric(
        "Molecular Weight",
        f"{Mmix:.2f} g/mol"
    )

with col6:

    st.metric(
        "Gas Constant",
        f"{Rs_mix:.2f} J/kg.K"
    )

with col7:

    st.metric(
        "Density",
        f"{rho:.2f} kg/m3"
    )

st.metric(
    "Z Factor",
    f"{Z:.3f}"
)

# =========================================================
# DATAFRAME
# =========================================================

st.header("Gas Composition Table")

st.dataframe(
    df,
    use_container_width=True
)

# =========================================================
# PDF FUNCTION
# =========================================================

def generate_pdf():

    report_date = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    doc = SimpleDocTemplate(
        "Gas_Report.pdf"
    )

    styles = getSampleStyleSheet()

    elements = []

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
    # NOTE
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

# =========================================================
# EXPORT PDF
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
            file_name="Gas_Report.pdf"
            mime="application/pdf"
        )
    st.success("Pdf generated successfully")
