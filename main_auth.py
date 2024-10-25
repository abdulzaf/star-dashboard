#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 23:13:58 2024

@author: abdulzaf
"""
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

names = ['Universite de Montreal', 'Sherbrooke']
usernames = ['udemontreal', 'sherbrooke']

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# name, authentication_status, username = authenticator.login('sidebar')
name, authentication_status, username = authenticator.login('main', fields = {'Form name': 'custom_form_name'})

if authentication_status:
    authenticator.logout('main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')