import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def home_page():
    st.title("Daily Reading Data")

    conn = st.connection("gsheets", type=GSheetsConnection)
    pages_by_date = conn.read(worksheet="Pages by Date")
    pages_by_date['date'] = pd.to_datetime(pages_by_date['date'])
    st.line_chart(pages_by_date, x="date", y="pages")

    st.header("Stats at a Glance")

pg = st.navigation([home_page, "add_new_reading.py", "view_reading_data.py"])
pg.run()