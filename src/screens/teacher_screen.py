import streamlit as st

from src.database.db import check_teacher_exists, create_teacher, teacher_login

def teacher_screen():
    st.header("Teacher Screen")
    
    

    if 'teacher_login_type' not in st.session_state or st.session_state['teacher_login_type'] == 'login':
       teacher_screen_login()
    elif st.session_state['teacher_login_type'] == 'register':
        teacher_screen_register()


def create_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm):
    if not teacher_username or not teacher_name or not teacher_password or not teacher_password_confirm:
        return False, "All fields are required."
    if check_teacher_exists(teacher_username):
        return False, "Username already exists."
    if teacher_password != teacher_password_confirm:
        return False, "Passwords do not match."
    try:
        create_teacher(teacher_username, teacher_name, teacher_password)
        st.session_state['teacher_login_type'] = 'login'
        return True, "Registration successful. You can now log in."
    except Exception as e:
        return False, "Unexpected error!"


def teacher_screen_login():
    col1, col2 = st.columns(2)
    with col2:
        if st.button("Back to home", key="loginbackbtn"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login as Teacher")

    teacher_username = st.text_input("Enter Username")
    teacher_password = st.text_input("Enter Password", type="password")

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Login Now", key="teacherloginbtn"):
            if teacher_login(teacher_username, teacher_password):
                st.toast("Login successful!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password.")
    with btnc2:
        if st.button("Register Instead", key="teacherregisterbtn"):
            st.session_state['teacher_login_type'] = 'register'
            st.rerun()



def teacher_screen_register():
    col1, col2 = st.columns(2)
    with col2:
        if st.button("Back to home", key="loginbackbtn"):
            st.session_state['login_type'] = None
            st.rerun()

    teacher_username = st.text_input("Enter Username")
    teacher_name = st.text_input("Enter Name")
    teacher_password = st.text_input("Enter Password", type="password")
    teacher_password_confirm = st.text_input("Confirm Password", type="password")

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Register Now", key="teacherloginbtn"):
            success, message = create_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm)
            if success:
                st.success(message)
                import time 
                time.sleep(2)
                st.session_state['teacher_login_type'] = 'login'
                st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button("Login Instead", key="teacherregisterbtn"):
            st.session_state['teacher_login_type'] = 'login'
            st.rerun()
    