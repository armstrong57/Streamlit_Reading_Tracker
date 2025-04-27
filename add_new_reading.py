import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Daily Reading Data App")

conn = st.connection("gsheets", type=GSheetsConnection)

if 'reading_data' not in st.session_state:
    reading_data = conn.read(worksheet='Reading Entries')
    st.session_state.reading_data = reading_data
else:
    reading_data = st.session_state.reading_data

st.write("Add new entry:")

new_date = st.date_input("Date")

all_titles = reading_data['title'].astype(str).to_list()
all_titles = list(set(all_titles))
all_titles.sort()
all_titles.insert(0, 'New Title')
title_select = st.selectbox("Book title", all_titles)
if (title_select == 'New Title'):
    new_title = st.text_input("Book Title")
else:
    new_title = title_select

new_pages = st.number_input("Pages read", step=1)

new_entry = pd.DataFrame(data={"date": new_date, "title": new_title, "pages": new_pages}, index=[reading_data.size])

if st.button("Add reading"):
    reading_data = pd.concat([reading_data, new_entry])
    reading_data = conn.update(data=reading_data)
    st.session_state.reading_data = reading_data
