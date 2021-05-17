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
st.image('logo.png')
sidebar = st.sidebar

analysis = Analyse("dataset/Environment_Temperature_change.csv")


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


def viewForm():

    st.plotly_chart(plot())

    title = st.text_input("Report Title")
    desc = st.text_area('Report Description')
    btn = st.button("Submit")

    if btn:
        report1 = Report(title=title, desc=desc, data="")
        sess.add(report1)
        sess.commit()
        st.success('Report Saved')


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

<<<<<<< HEAD
    selMon = st.selectbox(options = analysis.getMonths(), label=" Month")
    countries = ['USA','India','UK','Germany','Canada','Australia','Ireland','Europe','Japan']
=======
    st.text("Description here")
>>>>>>> 5f494d622ca8df6250ca1033f24988e6be1afaf8

    st.markdown("---")

    selMon = st.selectbox(
        options=['spring', 'fall', 'winter', 'summer'], label=" Season")
    countries = ['USA', 'INDIA', 'UK', 'GERMANY', 'CANADA', 'AUSTRALIA']

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


def viewReport():
    reports = sess.query(Report).all()
    titlesList = [report.title for report in reports]
    selReport = st.selectbox(options=titlesList, label="Select Report")

    reportToView = sess.query(Report).filter_by(title=selReport).first()

    markdown = f"""
        ## {reportToView.title}
        ### {reportToView.desc}
        
    """

    st.markdown(markdown)


sidebar.header('Choose Your Option')
options = ['View Dataset', 'Analyse Temperature', 'View Report']
choice = sidebar.selectbox(options=options, label="Choose Action")

if choice == options[0]:
    viewDataset()
elif choice == options[1]:
    analyseTemperature()
elif choice == options[2]:
    viewReport()
