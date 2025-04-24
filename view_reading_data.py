import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

st.title("View Reading Data")

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(1)
date_range = st.date_input("Select dates to view", [start_date, end_date])
if len(date_range) == 2:
    start_date, end_date = date_range
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

conn = st.connection("gsheets", type=GSheetsConnection)
reading_data = conn.read(worksheet='Reading Entries')
reading_data['date'] = pd.to_datetime(reading_data['date'])
mask = (reading_data['date'] >= start_date) & (reading_data['date'] <= end_date)
st.dataframe(reading_data.loc[mask], column_config={"date": st.column_config.DatetimeColumn(format="MMM D, YYYY")})
