import streamlit as st
st.set_page_config(layout="wide", page_title='LAS Explorer v.0.1')

from mo import local_css
import lasio
import missingno as mno
import pandas as pd
# Local Imports
from mo import home
from mo import raw_data
from mo import plot
from mo import header
from mo import missing
from io import StringIO



@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.read()
            str_io = StringIO(bytes_data.decode('Windows-1252'))
            las_file = lasio.read(str_io)
            well_data = las_file.df()
            well_data['DEPTH'] = well_data.index

        except UnicodeDecodeError as e:
            st.error(f"error loading log.las: {e}")
    else:
        las_file = None
        well_data = None

    return las_file, well_data


#TODO
def missing_data():
    st.title('Missing Data')
    missing_data = well_data.copy()
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    import plotly.express as px
    missing = px.area(well_data, x='DEPTH', y='DT')
    st.plotly_chart(missing)

# Sidebar Options & File Uplaod
las_file = None
st.sidebar.write('# LAS Data Explorer')
st.sidebar.write('To begin using the app, load your LAS file using the file upload option below.')

uploadedfile = st.sidebar.file_uploader(' ', type=['.las'])
las_file, well_data = load_data(uploadedfile)

if las_file:
    st.sidebar.success('File Uploaded Successfully')
    st.sidebar.write(f'<b>Well Name</b>: {las_file.well.WELL.value}',unsafe_allow_html=True)


# Sidebar Navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select a page:', 
    ['Home', 'Header Information', 'Data Information', 'Data Visualisation', 'Missing Data Visualisation'])

if options == 'Home':
    home()
elif options == 'Header Information':
    header(las_file)
elif options == 'Data Information':
    raw_data(las_file, well_data)
elif options == 'Data Visualisation':
    plot(las_file, well_data)
elif options == 'Missing Data Visualisation':
    missing(las_file, well_data)

