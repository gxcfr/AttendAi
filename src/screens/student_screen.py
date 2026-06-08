import time

from src.pipelines.face_pipeline import predict_attendance, get_face_embedding, train_classifier
from src.database.db import get_all_students, create_student
import streamlit as st 
import numpy as np
from PIL import Image

def student_dashboard():
    st.header("Student Dashboard")



def student_screen():

    if "student_data" in st.session_state:
        student_dashboard()
        return
    col1, col2 = st.columns(2)
    with col2:
        if st.button("Back to home", key="loginbackbtn"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login as Student")

    show_registration = False
    photosource = st.camera_input("Position your face in the frame and take a picture.")

    if photosource:
        img = np.array(Image.open(photosource))

        with st.spinner("Processing..."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.error("No face detected. Please try again.")
            elif num_faces > 1:
                st.error("Multiple faces detected. Please ensure only one face is in the frame.")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students() 
                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.success(f"Welcome, {student['name']}!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized. You might be a new student.")
                    show_registration = True 
   
    if show_registration:
        with st.container():
            st.header("Student Registration")
            new_name = st.text_input("Enter your name")
            
            if st.button("create account", type="primary"):
                if new_name:
                    with st.spinner("Creating account..."):
                        img = np.array(Image.open(photosource))
                        encodings = get_face_embedding(img) 
                        if encodings:
                            face_emb = encodings[0].tolist()

                            response_data = create_student(new_name, face_emb)

                            if response_data:
                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data
                                st.success(f"Profile created. HI, {new_name}!")
                                time.sleep(1)
                                st.rerun()
                        else: 
                            st.error("couldnt capture your facial features.")

                else: 
                    st.warning("Please enter your name to create an account.")
