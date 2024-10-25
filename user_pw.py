#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 23:02:22 2024

@author: abdulzaf
"""

import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ['Universite de Montreal', 'Sherbrooke']
usernames = ['udemontreal', 'sherbrooke']
passwords = ['udem2024', 'sher2024']

hashed_passwords = [stauth.Hasher(passwords).hash(pw) for pw in passwords]