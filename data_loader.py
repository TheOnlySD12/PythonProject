import gspread
import pandas as pd
import streamlit as st

link_test = "https://docs.google.com/spreadsheets/d/11_EX0jPsefpTAZnAzZtMq4dHjeg8qpZoN--wuQd8Fhg"

def get_worksheet():
    g = st.secrets["bot"]
    creds = {
        "type": g["type"],
        "project_id": g["project_id"],
        "private_key_id": g["private_key_id"],
        "private_key": g["private_key"].replace("\\n", "\n"),
        "client_email": g["client_email"],
        "client_id": g["client_id"],
        "auth_uri": g["auth_uri"],
        "token_uri": g["token_uri"],
        "auth_provider_x509_cert_url": g["auth_provider_x509_cert_url"],
        "client_x509_cert_url": g["client_x509_cert_url"],
        "universe_domain": g["universe_domain"],
    }
    gc = gspread.service_account_from_dict(creds)
    return pd.DataFrame(gc.open_by_url(link_test).get_worksheet(0).get_all_records())