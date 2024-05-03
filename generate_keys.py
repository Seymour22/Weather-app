import pickle
from pathlib import Path
import os
import pandas as pd
import streamlit_authenticator as stauth


userpw=pd.read_csv('userpw.csv')

names = userpw['Customer name']
usernames = userpw['Username']
passwords = userpw['Password']

hashed_passwords = stauth.Hasher(passwords).generate()
current_dir = os.getcwd()
file_path = Path(current_dir) / "hashed_pw.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

usernopw=userpw.copy()
del usernopw['Password']
usernopw.to_csv('usernopw.csv')
