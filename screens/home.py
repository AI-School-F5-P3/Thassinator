import streamlit as st
from utils.aux_functions import load_css, load_image

def change_screen(new_screen):
    st.session_state.screen = new_screen

def home_screen():
    load_css('style.css')

    image = load_image('logo 2.png')
    st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{image}" width="150">
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown("""
        <div class="service-box" style="text-align: center;">
        <h3>👥 Welcome to Thassinator, your automated face logger.</h3>
        <p>Simplify your workplace attendance management with our cutting-edge facial recognition system. Our application offers a seamless, contactless solution for tracking employee presence with maximum accuracy and security.</p>
        <p>Built with advanced machine learning algorithms and robust neural networks, our system provides reliable face detection and authentication in real-time, eliminating the need for traditional time cards or manual logging systems.</p>
        <p>Our solution ensures data privacy and secure storage of biometric information, complying with industry standards while offering a user-friendly interface for both administrators and employees.</p>
        <p>Transform your workplace attendance management into an efficient, modern, and trustworthy process with our automated face logging system.</p>
        </div>
        """, unsafe_allow_html=True)

    # Servicios
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>Our Services</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="service-box">
        <h3>Easy Access Management</h3>
        <p>Experience seamless attendance tracking with our user-friendly interface. Simply walk in front of the camera, and our system instantly recognizes authorized personnel. Our comprehensive dashboard provides real-time attendance logs, making it effortless to monitor workplace presence and manage access permissions for your entire team.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="service-box">
        <h3>Security & Tracking</h3>
        <p>Stay secure with our advanced logging system. Track all access attempts, monitor successful and denied entries, and maintain detailed records of employee attendance patterns. Get instant notifications of unauthorized access attempts and generate comprehensive reports for attendance analysis and security audits.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center;">
            <h4>Our system is designed to streamline your workplace access control while maintaining the highest security standards. View attendance patterns, manage permissions, and monitor security all from one central dashboard.</h4>
            <h4>Transform your workplace security with intelligent, automated face recognition technology that you can trust.</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Replace the existing button with centered columns
    col1, col2, col3 = st.columns([3, 2, 3])
    
    with col2:
        if st.button("Start the event", use_container_width=True):
            change_screen('LogIn')