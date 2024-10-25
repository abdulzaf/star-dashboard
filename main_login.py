# streamlit_app.py

import hmac
import streamlit as st
import pandas as pd
import altair as alt
from streamlit_dynamic_filters import DynamicFilters
from streamlit_gsheets import GSheetsConnection

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            st.session_state["user"] = st.session_state["username"]
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False

if not check_password():
    st.stop()
else:
    # Main Streamlit app starts here
    team = st.session_state['user']    
    # get data URL
    
    if team=='udemontreal':
        conn = st.connection("udem", type=GSheetsConnection)
    elif team=='sherbrooke':
        conn = st.connection("sher", type=GSheetsConnection)

    def load_data():
        print(team)
        data = conn.read()
        # data = pd.read_csv(DATA_URL)
        data.Date = pd.to_datetime(data.Date)
        data['HRper'] = 100 * data.HR_o85 / data.HR_u85
        return data
    
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = load_data()
    # Notify the reader that the data was successfully loaded.
    data_load_state.text(f'Team Dashboard: {team}')
    
    # filters
    dynamic_filters = DynamicFilters(data, filters=['Date', 'Role', 'Position', 'Player Name'])
    dynamic_filters.display_filters(location='sidebar')
    data_filt = dynamic_filters.filter_df()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Speed", "Power", "Conditioning", "Raw"])

    with tab1:
        # tab1.line_chart(data=data, x='Date', y='Maximum Velocity')
        line = alt.Chart(data_filt).mark_line().encode(
            alt.X('Date:T', axis=alt.Axis(format="%Y %B")),
            # x='Date',
            y=alt.Y("mean(Maximum Velocity)", scale=alt.Scale(domain=[12, 35])),
        )
        band = alt.Chart(data_filt).mark_errorband(extent='ci').encode(
            x='Date',
            y=alt.Y("Maximum Velocity", scale=alt.Scale(domain=[12, 35])),
        )
        
        vbar = alt.Chart(data_filt).transform_fold(
          ['Velocity Band 3 Total Distance', 'Velocity Band 4 Total Distance', 'Velocity Band 5 Total Distance', 'Velocity Band 6 Total Distance'],
          as_=['Speed Zone', 'Distance']
        ).mark_bar(cornerRadius=8, width=20).encode(
            alt.X('Date:T', axis=alt.Axis(format="%Y %B")),
            y=alt.Y('mean(Distance):Q', scale=alt.Scale(domain=[0, 1000])),
            order=alt.Order('key:N',sort='descending'),
            color=alt.Color('Speed Zone:N', legend=alt.Legend(
                orient='bottom',
                direction='horizontal',
                titleAnchor='middle')).scale(scheme="lighttealblue")
        )
        
        st.subheader("Speed")
        st.altair_chart(line + band, use_container_width=True)
        st.subheader("Distance by speed zone")
        st.altair_chart(vbar, use_container_width=True)
    with tab2:
        pbar = alt.Chart(data_filt).mark_bar(cornerRadius=8, width=20, color='#c8a85a').encode(
            x=alt.X('Date:T', axis=alt.Axis(format="%Y %B")),
            y=alt.Y('mean(Peak Meta Power)', title='Maximum Power'),
        )
        effbar = alt.Chart(data_filt).mark_bar(cornerRadius=8, width=20, color='#c8a85a').encode(
            y=alt.X('min(Explosive Efforts):Q'),
            y2='max(Explosive Efforts):Q',
            x=alt.Y('Date:T')
        )
        text_min = alt.Chart(data_filt).mark_text(align='center', dy=-10).encode(
            y='min(Explosive Efforts):Q',
            x=alt.X('Date:T'),
            text='min(Explosive Efforts):Q'
        )
        
        text_max = alt.Chart(data_filt).mark_text(align='center', dy=10).encode(
            y='max(Explosive Efforts):Q',
            x=alt.X('Date:T'),
            text='max(Explosive Efforts):Q'
        )
        
        st.header("Power")
        st.altair_chart(pbar, use_container_width=True)
        st.altair_chart(effbar + text_min + text_max, use_container_width=True)
        # st.altair_chart(line1 + band1, use_container_width=True)
    with tab3:
        hbar = alt.Chart(data_filt).mark_bar(cornerRadius=8, width=20, color='#C34B3E').encode(
            x=alt.X('Date:T', axis=alt.Axis(format="%Y %B")),
            y=alt.Y('mean(Maximum Heart Rate)', title='Max HR'),
        )
        lineh = alt.Chart(data_filt).mark_line(color='#C34B3E').encode(
            alt.X('Date:T', axis=alt.Axis(format="%Y %B")),
            # x='Date',
            y=alt.Y("mean(Mean Heart Rate)", title='Mean HR')#, scale=alt.Scale(domain=[12, 35])),
        )
        line1 = alt.Chart(data_filt).mark_line(color='#C34B3E').encode(
            alt.X('Date:T', axis=alt.Axis(format="%Y %B")),
            # x='Date',
            y=alt.Y("mean(HRper)", title='% time above 85%HRMax')#, scale=alt.Scale(domain=[12, 35])),
        )
        band1 = alt.Chart(data_filt).mark_errorband(extent='ci', color='#C34B3E').encode(
            x='Date',
            y=alt.Y("HRper"),
        )
        st.header("Conditioning")
        st.altair_chart(lineh + hbar, use_container_width=True)
        st.altair_chart(line1 + band1, use_container_width=True)
    with tab4:
        st.header('Raw data')
        st.write(data_filt)
