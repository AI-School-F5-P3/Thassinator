import streamlit as st
from utils.aux_functions import load_css, load_image

def about_screen():
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
        <div class="service-box">
            <h2>About Thassinator</h2>
            <p>Born from the vision of creating seamless, secure access control, Thassinator represents the pinnacle of AI-powered facial recognition technology. Our journey began in 2023 when a team of passionate engineers and security experts came together to revolutionize event access management.</p>
        </div>
        
        <div class="service-box">
            <h3>Our Mission</h3>
            <p>To provide cutting-edge facial recognition solutions that make secure access control effortless while maintaining the highest standards of privacy and data protection.</p>
        </div>
        
        <div class="service-box">
            <h3>Technology</h3>
            <p>Powered by advanced neural networks and state-of-the-art computer vision algorithms, Thassinator processes facial features in milliseconds, providing instant access decisions with remarkable accuracy. Our system employs:</p>
            <ul>
                <li>Deep learning facial recognition</li>
                <li>Real-time video processing</li>
                <li>Encrypted data storage</li>
                <li>Automated logging and reporting</li>
            </ul>
        </div>
        
        <div class="service-box">
            <h3>Privacy First</h3>
            <p>We understand the importance of data privacy. That's why Thassinator implements industry-leading security measures:</p>
            <ul>
                <li>Secure template storage</li>
                <li>No permanent image storage</li>
                <li>End-to-end encryption</li>
                <li>Compliance with privacy regulations</li>
            </ul>
        </div>
        
        <div class="service-box">
            <h3>The Team</h3>
            <p>Thassinator is developed by Thassination Technologies, a forward-thinking company dedicated to advancing security through innovation. Our team combines expertise in artificial intelligence, computer vision, and security systems to deliver a product that sets new standards in access control.</p>
        </div>
    """, unsafe_allow_html=True)