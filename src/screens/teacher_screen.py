import streamlit as st 

def teacher_screen():
    st.header("Teacher Screen")
    
    

    if 'teacher_login_type' not in st.session_state or st.session_state['teacher_login_type'] == 'login':
       teacher_screen_login()
    elif st.session_state['teacher_login_type'] == 'register':
        teacher_screen_register()


    

    


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
        st.button("Login Now", key="teacherloginbtn")
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
        st.button("Register Now", key="teacherloginbtn")
    with btnc2:
        if st.button("Login Instead", key="teacherregisterbtn"):
            st.session_state['teacher_login_type'] = 'login'
            st.rerun()
    