import streamlit as st

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from database import Report
from visualization import *
from AnalyseData import Analyse

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

st.title('Global Warming and Climate Change Analysis')
sidebar = st.sidebar

@st.cache(suppress_st_warning=True)
def loadData():
    return Analyse("dataset/Environment_Temperature_change.csv"), Analyse("dataset/natural-disaster-events.csv"), Analyse("dataset/sea_levels.csv"), Analyse("dataset/flood_damage.xls")

analysis, disasterAnalysis, seaAnalysis, floodAnalysis = loadData()


def viewDataset():
    st.header('Data Used in Project')
    dataframe = analysis.getDataframe()

    with st.spinner("Loading Data..."):
        st.dataframe(dataframe)

        st.markdown('---')
        cols = st.beta_columns(4)
        cols[0].markdown("### No. of Rows :")
        cols[1].markdown(f"# {dataframe.shape[0]}")
        cols[2].markdown("### No. of Columns :")
        cols[3].markdown(f"# {dataframe.shape[1]}")
        st.markdown('---')

        st.header('Summary')
        st.dataframe(dataframe.describe())
        st.markdown('---')

        types = {'object': 'Categorical',
                 'int64': 'Numerical', 'float64': 'Numerical'}
        types = list(map(lambda t: types[str(t)], dataframe.dtypes))
        st.header('Dataset Columns')
        for col, t in zip(dataframe.columns, types):
            st.markdown(f"### {col}")
            cols = st.beta_columns(4)
            cols[0].markdown('#### Unique Values :')
            cols[1].markdown(f"# {dataframe[col].unique().size}")
            cols[2].markdown('#### Type :')
            cols[3].markdown(f"## {t}")


def analyseTemperature():
    st.header('Average Temperature rise in Countries')
    selConl = st.selectbox(options=analysis.getCountries(), label="Country")

    col1, col2 = st.beta_columns(2)
    data1 = analysis.country_df(selConl)
    with st.spinner('Loading Plot...'):
        col1.plotly_chart(plotLine(data1, 'year', 'Meteorological year',
                                   title="Line Chart"))

    data2 = analysis.country_df(selConl)
    with st.spinner('Loading Plot...'):
        col2.plotly_chart(
            plotBar(data2, 'year', 'Meteorological year', title="Bar Chart"))

    selMon = st.selectbox(options=analysis.getMonths(), label=" Month")
    countries = ['USA', 'India', 'UK', 'Germany', 'Canada',
                 'Australia', 'Ireland', 'Europe', 'Japan']

    st.text("Description here")

    st.markdown("---")

    selMon = st.selectbox(
        options=['spring', 'fall', 'winter', 'summer'], label=" Season")
    countries = ['USA', 'INDIA', 'UK', 'GERMANY', 'CANADA',
                 'AUSTRALIA', 'Ireland', 'Europe', 'Japan']

    selcountry = st.selectbox(options=countries, label=" Country")
    st.image(f'plotImages/{selcountry}_{selMon}.png')

    st.header('Average Temperature rise in seasons')
    st.image('plotImages/temp_shift.png')

    st.header('Comparing the World Temperature with respect to years')
    st.image('plotImages/world_line.png')

    st.header('Comparing the Country Temperatures with respect to years')
    st.image('plotImages/world_line.png')

    st.header('Continental temperature rise in various seasons')
    st.image('plotImages/season_continent.png')


def analyseFloods():
    st.header('Flood Damage India')
    st.plotly_chart(plotLine(floodAnalysis.getDataframe(),
                             'Year', 'Area affected-India', title="Total Area Damaged in India"))

    st.plotly_chart(plotLine(floodAnalysis.getDataframe(),
                             'Year', 'Population affected-India', title="Total Population Affected in India"))

    st.plotly_chart(plotLine(floodAnalysis.getDataframe(),
                             'Year', 'Human lost no.-India', title="Total Humans loss in India"))

    st.plotly_chart(plotLine(floodAnalysis.getDataframe(),
                             'Year', 'Damage C.area-Bihar', title="Total Crop Affected in Bihar"))

    st.plotly_chart(plotLine(floodAnalysis.getDataframe(),
                             'Year', 'Total damage crops,Houses & Public utilities in Rs.crore', title="Total damage in Bihar"))

    st.plotly_chart(plotGroupedBar(floodAnalysis.getAreaData(
    ), ('India', 'Bihar', 'Uttar Pradesh', 'Madhya Pradesh'), title="Comparison of Crops Area damaged"))

    st.plotly_chart(plotGroupedBar(floodAnalysis.getPopulationData(
    ), ('India', 'Bihar', 'Uttar Pradesh', 'Madhya Pradesh'), title="Comparison of Population Affected"))


def analyseDisasters():

    st.markdown("#")
    st.header('Analysis of Natural Disasters')
    st.markdown('---')
    data = disasterAnalysis.getDisasterType()
    st.plotly_chart(plotBar(data, 'Entity', 'Year',
                            title="Types of Natural Disasters"))

    data = disasterAnalysis.getDisasterCount()
    st.plotly_chart(plotPie(data.values, data.index, title="No. of Disasters"))

    data = disasterAnalysis.getDisasterByYear()
    st.plotly_chart(plotLine(data, 'Year', 'disasters',
                             title='Disasters per Year'))


def analyseSeaLevel():
    st.header('Sea Levels')
    data = seaAnalysis.getDataframe()
    st.plotly_chart(plotLine(data, 'Time', 'GMSL',
                          title = "Sea level Rise in by months of Years "))

    st.plotly_chart(plotBar(data, 'Time', 'GMSL',
                            title="Sea Level Rise in by months of Years"))

    st.plotly_chart(plotBar(seaAnalysis.getAvgSeaLevelRise(),
                            'Year', 'GMSL', title="Averge Sea Level Rise Every Year"))

    st.plotly_chart(plotBar(seaAnalysis.getMinSeaLevelRise(),
                            'Year', 'GMSL', title="Minimum Sea Level Rise Every Year"))

    st.plotly_chart(plotBar(seaAnalysis.getMaxSeaLevelRise(),
                            'Year', 'GMSL', title="Maximum Sea Level Rise Every Year"))
                        


sidebar.header('Choose Your Option')
options = ['View Dataset', 'Analyse Climate', 'Analyse Floods',
           'Analyse other Disasters', 'Analyse Sea Level']
choice = sidebar.selectbox(options=options, label="Choose Action")

if choice == options[0]:
    viewDataset()
elif choice == options[1]:
    analyseTemperature()
elif choice == options[2]:
    analyseFloods()
elif choice == options[3]:
    analyseDisasters()
elif choice == options[4]:
    analyseSeaLevel()
