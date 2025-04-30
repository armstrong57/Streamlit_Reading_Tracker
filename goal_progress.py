import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import utils

end_date = datetime.datetime.now()
start_date = datetime.date(datetime.date.today().year, 1, 1)
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

year_percent = utils.calculate_year_percent(end_date)

conn = st.connection("gsheets", type=GSheetsConnection)
reading_data = conn.read(worksheet='ReadingEntries')
reading_data['date'] = pd.to_datetime(reading_data['date'])
mask = (reading_data['date'] >= start_date) & (reading_data['date'] <= end_date)
reading_in_range = reading_data.loc[mask]

goal_metric = st.selectbox("Goal Metric", ("Pages", "Books"))
goal_number = st.number_input("Goal", value=12000, min_value=1, step=1)
target_now = goal_number * year_percent

pages_col = reading_in_range['pages'].to_list()
page_count = sum(pages_col)

book_count = reading_in_range['title'].nunique()

on_track = False
if goal_metric == "Pages":
    goal_current = page_count
    goal_completion = min(float(page_count) / float(goal_number), 1)
    if page_count > target_now:
        on_track = True
elif goal_metric == "Books":
    goal_current = book_count
    goal_completion = min(float(book_count) / float(goal_number), 1)
    if book_count > target_now:
        on_track = True

st.write("Goal Progress: **{:.3f}%** ({} out of {})".format(goal_completion*100, int(goal_current), goal_number))
st.progress(goal_completion, text="Goal Progress")

if on_track:
    st.write("You are **on track**! :tada:")
else:
    st.write("You're running behind! :fearful: :running:")
