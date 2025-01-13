import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st

def setup_authenticator(config_path):
    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        auto_hash=True
    )
    try:
        authenticator.login()
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)

    return authenticator
