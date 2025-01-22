import streamlit as st
from utils.aux_functions import load_css, load_image

def change_screen(new_screen):
    st.session_state.screen = new_screen

def login_screen():
    load_css('style.css')
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    image = load_image('logo 2.png')
    st.markdown(
        f"""<div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{image}" width="150">
        </div>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center;">
            <h2>Log In</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        # Replace with your actual authentication logic
        if username == "admin" and password == "password":
            st.session_state.logged_in = True
            st.success("Login successful!")
            change_screen('Event Logger')
        else:
            st.error("Invalid username or password")
    
    return st.session_state.logged_in