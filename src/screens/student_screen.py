import streamlit as st 
from src.database.db import check_teacher_exists, create_teacher, teacher_login
import numpy as np
from PIL import Image

def student_screen():
    col1, col2 = st.columns(2)
    with col2:
        if st.button("Back to home", key="loginbackbtn"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login as Student")

    photosource = st.camera_input("Position your face in the frame and take a picture.")

    if photosource:
        np.array(Image.open(photosource))
    

   
   
    