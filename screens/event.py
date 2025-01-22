import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import time
from datetime import datetime
import pandas as pd
from utils.aux_functions import load_css, load_image
from thassinator import FrameProcessor, load_known_faces

def event_screen():
    # Clear the screen first
    st.empty()
    load_css('style.css')
    
    # Initialize session state
    if 'logging_active' not in st.session_state:
        st.session_state.logging_active = False
    if 'cap' not in st.session_state:
        st.session_state.cap = None
    if 'last_logged' not in st.session_state:
        st.session_state.last_logged = {}
    
    # Create logs directory and file
    logs_dir = "access_logs"
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, f"access_log.csv")
    
    if not os.path.exists(log_file):
        pd.DataFrame(columns=['timestamp', 'name', 'status']).to_csv(log_file, index=False)
    
    # Create snapshots directory
    snapshots_dir = "access_snapshots"
    granted_dir = os.path.join(snapshots_dir, "granted")
    denied_dir = os.path.join(snapshots_dir, "denied")
    os.makedirs(granted_dir, exist_ok=True)
    os.makedirs(denied_dir, exist_ok=True)
    
    # Create containers for different parts of the UI
    header_container = st.container()
    control_container = st.container()
    video_container = st.container()
    
    with header_container:
        # Display logo
        image = load_image('logo 2.png')
        st.markdown(
            f"""<div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{image}" width="150">
            </div>""",
            unsafe_allow_html=True
        )
    
    with control_container:
        # Center the buttons with custom widths
        col1, col2, col3 = st.columns([3, 2, 3])
        
        with col2:
            if not st.session_state.logging_active:
                st.button("Start Logging", 
                         type="primary", 
                         key="start_button",
                         use_container_width=True,
                         on_click=lambda: setattr(st.session_state, 'logging_active', True))
            else:
                st.button("Stop Logging", 
                         type="secondary",
                         key="stop_button", 
                         use_container_width=True,
                         on_click=lambda: [
                             st.session_state.cap.release() if st.session_state.cap else None,
                             setattr(st.session_state, 'cap', None),
                             setattr(st.session_state, 'logging_active', False)
                         ])
    
    if st.session_state.logging_active:
        known_face_encodings, known_face_names = load_known_faces("known_faces")
        frame_processor = FrameProcessor(known_face_encodings, known_face_names)
        
        with video_container:
            video_placeholder = st.empty()
            
        # Add log table container below video
        log_container = st.container()
        with log_container:
            st.markdown(
                """
                <div class="title">
                    <h3>Recent Granted Access</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Load and filter access logs
            if os.path.exists(log_file):
                df = pd.read_csv(log_file)
                granted_df = df[df['status'] == 'ACCESS GRANTED'].copy()
                granted_df['timestamp'] = pd.to_datetime(granted_df['timestamp'])
                granted_df = granted_df.sort_values('timestamp', ascending=False).head(5)
                granted_df = granted_df[['timestamp', 'name']]  # Show only relevant columns
                
                st.markdown('<div class="table-wrapper">', unsafe_allow_html=True)
                st.markdown('<div class="table-container">', unsafe_allow_html=True)
                st.table(granted_df)
                st.markdown('</div></div>', unsafe_allow_html=True)
        
        if st.session_state.cap is None:
            st.session_state.cap = cv2.VideoCapture(0)
        
        try:
            while st.session_state.logging_active:
                ret, frame = st.session_state.cap.read()
                if not ret:
                    st.error("Failed to access webcam")
                    break
                    
                results = frame_processor.process_frame(frame)
                
                for result in results:
                    top, right, bottom, left = result["location"]
                    color = (0, 255, 0) if result["status"] == "ACCESS GRANTED" else (0, 0, 255)
                    
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.rectangle(frame, (left, bottom - 45), (right, bottom), color, cv2.FILLED)  # Increased height from 35 to 45
                    cv2.putText(frame, f"{result['status']} ({int(result['confidence'])}%)",
                               (left + 6, bottom - 15),  # Changed y-position from -6 to -15
                               cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)  # Reduced font size from 0.6 to 0.5
                    
                    person_id = result["name"]
                    current_time = time.time()
                    
                    if (person_id not in st.session_state.last_logged or
                        current_time - st.session_state.last_logged[person_id] > 300):
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Use : instead of - for time
                        new_log = pd.DataFrame({
                            'timestamp': [timestamp],  # Remove replace() since format is already correct
                            'name': [result["name"]],
                            'status': [result["status"]]
                        })
                        
                        # Save full frame snapshot in access folders
                        snapshot_dir = granted_dir if result["status"] == "ACCESS GRANTED" else denied_dir
                        filename = f"{result['name']}_{timestamp}.jpg"
                        snapshot_path = os.path.join(snapshot_dir, filename)
                        cv2.imwrite(snapshot_path, frame)
                        
                        # Save only face region for future testing
                        if result["name"] != "Unknown":
                            # Extract face with some padding
                            top, right, bottom, left = result["location"]
                            padding = 30
                            face_top = max(top - padding, 0)
                            face_bottom = min(bottom + padding, frame.shape[0])
                            face_left = max(left - padding, 0)
                            face_right = min(right + padding, frame.shape[1])
                            face_image = frame[face_top:face_bottom, face_left:face_right]
                            
                            # Save face snapshot
                            user_dir = os.path.join("future_test", result["name"])
                            os.makedirs(user_dir, exist_ok=True)
                            user_snapshot_path = os.path.join(user_dir, filename)
                            cv2.imwrite(user_snapshot_path, face_image)
                        
                        new_log.to_csv(log_file, mode='a', header=False, index=False)
                        st.session_state.last_logged[person_id] = current_time
                        
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(frame_rgb, channels="RGB")
                time.sleep(0.1)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            if st.session_state.cap is not None:
                st.session_state.cap.release()
            st.session_state.cap = None
            st.session_state.logging_active = False