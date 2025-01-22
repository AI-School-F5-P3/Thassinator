import streamlit as st
from utils.aux_functions import load_css, load_image
import pandas as pd
from pathlib import Path
import base64
import os

def get_image_as_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    except:
        return None

def attendees_screen():
    load_css('style.css')
    
    # Display logo
    image = load_image('logo 2.png')
    st.markdown(
        f"""<div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{image}" width="150">
        </div>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="title">
            <h2>Access Log Records</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load and display the access log as a table
    log_path = Path('access_logs/access_log.csv')
    org_path = Path('organigrama.csv')
    
    if log_path.exists():
        df = pd.read_csv(log_path)
        
        # Load organigrama and merge with access log
        if org_path.exists():
            org_df = pd.read_csv(org_path)
            df = df.merge(
                org_df[['name', 'position', 'department']], 
                on='name', 
                how='left'
            )
        else:
            df['position'] = 'N/A'
            df['department'] = 'N/A'
        
        # Add snapshot column
        df['snapshot'] = df.apply(lambda row: 
            get_image_as_base64(
                os.path.join(
                    'access_snapshots',
                    'granted' if row['status'] == 'ACCESS GRANTED' else 'denied',
                    f"{row['name']}_{row['timestamp'].replace(' ', '_')}.jpg"
                )
            ), axis=1)
        
        # Convert snapshot column to HTML img tags
        df['snapshot'] = df['snapshot'].apply(lambda x: 
            f'<img src="{x}" width="100px">' if x else 'No image')
        
        # Reorder columns
        df = df[['timestamp', 'name', 'position', 'department', 'status', 'snapshot']]
        
        # Style the dataframe
        styled_df = df.style\
            .set_properties(**{
                'background-color': '#1a237e',
                'color': '#7ee7ff',
                'border': '1px solid #4fc3f7'
            })\
            .set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', '#283593'),
                    ('color', '#7ee7ff'),
                    ('font-family', 'Montserrat'),
                    ('font-weight', 'bold'),
                    ('border', '1px solid #4fc3f7')
                ]}
            ])\
            .format({'snapshot': lambda x: x})
        
        # Wrap table in centering container
        st.markdown('<div class="table-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.warning("No access log found.")