import streamlit as st

def style_background_dashboard():
    st.markdown(
        """
        <style>
            .stApp {
                background: #CEE5ED !important;
                }
        
        </style>
        """, unsafe_allow_html=True
    )


def style_background_home():
    st.markdown(
        """
        <style>
            .stApp {
                background: #CEE5ED !important;
                }
        
        </style>
        """, unsafe_allow_html=True
    )


def style_base_layout():
    st.markdown(
        """
        <style>
        /*Hide toolbar */
            #MainMenu, footer, header {visibility: hidden;}              
        </style>
        """, unsafe_allow_html=True
    )