import streamlit as st

from src.database.db import check_teacher_exists, create_teacher, teacher_login

def teacher_screen():
    st.header("Teacher Screen")
    
    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state['teacher_login_type'] == 'login':
       teacher_screen_login()
    elif st.session_state['teacher_login_type'] == 'register':
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state['teacher_data']
    st.write(f"Welcome, {teacher_data['name']}!")
    st.write("This is your teacher dashboard.")
    if st.button("Logout"):
        del st.session_state['teacher_data']
        st.session_state['teacher_login_type'] = 'login'
        st.rerun()

def register_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm):
    if not teacher_username or not teacher_name or not teacher_password or not teacher_password_confirm:
        return False, "All fields are required."
    if check_teacher_exists(teacher_username):
        return False, "Username already exists."
    if teacher_password != teacher_password_confirm:
        return False, "Passwords do not match."
    
    if create_teacher(teacher_username, teacher_name, teacher_password):
        st.session_state['teacher_login_type'] = 'login'
        return True, "Registration successful. You can now log in."
   
def login_teacher(teacher_username, teacher_password):
    if not teacher_username or not teacher_password:
        st.error("Please enter both username and password.")
        return False
    teacher = teacher_login(teacher_username, teacher_password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state['teacher_data'] = teacher
        st.session_state.is_logged_in = True   
        return True
    return False


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
            if login_teacher(teacher_username, teacher_password):
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
            success, message = register_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm)
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
    