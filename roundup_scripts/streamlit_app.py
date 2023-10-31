# This is where the app will be.
# Helpful tutorial: https://python-textbook.pythonhumanities.com/05_streamlit/05_01_03_displaying_data.html

import streamlit as st
import pandas as pd

# Title of the app
st.title('Roundup Data Viewer')
st.header('The latest economics working papers')
st.subheader('E pluribus unum.')
html = """
<a style='background:yellow'>Displayed are the most recent working paper publications from 18 websites.</a>
"""
st.markdown(html, unsafe_allow_html=True)
#st.set_page_config(layout="wide")

# GitHub raw URL of the CSV file
csv_url = 'https://raw.githubusercontent.com/lorae/roundup/main/historic/papers-we-have-seen-metadata.csv'

# Read and display the CSV file
df = pd.read_csv(csv_url)

# Remove the 'Number' column
df = df.drop(columns=['Number'])

# Create hyperlinks for the 'Title' column using the 'Link' column
df['Title'] = df.apply(lambda row: f"[{row['Title']}]({row['Link']})", axis=1)

# Remove the 'Link' column
df = df.drop(columns=['Link'])

# Sidebar
st.sidebar.header("Sidebar Header")

# Data frame
st.dataframe(df, height = 750)

options = ["Red", "Blue", "Yellow"]
selectbox_selection = st.selectbox("Select Color", options)
st.write(f"Color selected is {selectbox_selection}")
