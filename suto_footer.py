import streamlit as st


def show_suto_footer():

    st.divider()

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#666666;
            font-size:12px;
            padding:10px;
        ">
        SUTO iTEC Indonesia<br>
        Industrial Natural Gas Constant Calculation<br>
        Version 1.1<br> 
        Created by Cahyadi Wisnu Wardana. MM
        </div>
        """,
        unsafe_allow_html=True
    )
