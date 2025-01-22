import streamlit as st
from screens.home import home_screen
from screens.event import event_screen
from screens.about import about_screen
from screens.login import login_screen
from screens.attendees import attendees_screen

st.set_page_config(
    page_title= "Thassinator",
    page_icon = "🔱",
    layout = 'wide'
)

if 'screen' not in st.session_state:
    st.session_state.screen = 'Home'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def change_screen(new_screen):
    st.session_state.screen = new_screen

st.sidebar.header('Navigation')
if st.sidebar.button('Home'):
    change_screen('Home')
if st.sidebar.button('Event Logger'):
    if not st.session_state.logged_in:
        change_screen('Login')
    else:
        change_screen('Event Logger')
if st.sidebar.button('Attendees'):
    if not st.session_state.logged_in:
        change_screen('Login')
    else:
        change_screen('Attendees')
if st.sidebar.button('About'):
    change_screen('About')

if st.session_state.screen == 'Home':
    home_screen()
elif st.session_state.screen == 'Event Logger':
    if st.session_state.logged_in:
        event_screen()
    else:
        change_screen('Login')
elif st.session_state.screen == 'Login':
    login_screen()
elif st.session_state.screen == 'Attendees':
    if st.session_state.logged_in:
        attendees_screen()
    else:
        change_screen('Login')
elif st.session_state.screen == 'About':
    about_screen()