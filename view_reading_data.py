import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import statistics

st.title("View Reading Data")

end_date = datetime.datetime.now()
start_date = datetime.date(datetime.date.today().year, 1, 1)
date_range = st.date_input("Select dates to view", [start_date, end_date])
if len(date_range) == 2:
    start_date, end_date = date_range
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

conn = st.connection("gsheets", type=GSheetsConnection)
reading_data = conn.read(worksheet='ReadingEntries')
pages_data = conn.read(worksheet='PagesbyDate')
reading_data['date'] = pd.to_datetime(reading_data['date'])
pages_data['date'] = pd.to_datetime(pages_data['date'])
mask_1 = (reading_data['date'] >= start_date) & (reading_data['date'] <= end_date)
mask_2 = (pages_data['date'] >= start_date) & (pages_data['date'] <= end_date)
reading_in_range = reading_data.loc[mask_1]
pages_in_range = pages_data.loc[mask_2]

st.header("Date range stats overview")

# Total pages read
pages_col = reading_data['pages'].to_list()
page_count = int(sum(pages_col))
st.write("Pages read: **{}**".format(page_count))

# Number books read
st.write("Books read: **{}**".format(reading_data['title'].nunique()))

# Highest reading day
pages_in_range = pages_in_range.set_index('date')
highest_page_count = pages_in_range['pages'].max()
highest_val = pages_in_range.idxmax()
highest_date = pd.to_datetime(highest_val).values[0].astype('datetime64[us]').astype('O')
st.write("Most pages read in one day: **{}** pages on {}".format(int(highest_page_count), highest_date.strftime("%b %d, %Y")))

# Lowest reading day
lowest_page_count = pages_in_range['pages'].min()
lowest_val = pages_in_range.idxmin()
lowest_date = pd.to_datetime(lowest_val).values[0].astype('datetime64[us]').astype('O')
st.write("Least pages read in one day: **{}** pages on {}".format(int(lowest_page_count), lowest_date.strftime("%b %d, %Y")))

# Average pages/day
pages_count_list = pages_in_range['pages'].to_list()
average_pages = statistics.fmean(pages_count_list)
st.write("Average pages per day: **{:.4f}**".format(average_pages))

st.header("All reading data for selected dates:")
st.dataframe(reading_in_range, column_config={"date": st.column_config.DatetimeColumn(format="MMM D, YYYY")})
