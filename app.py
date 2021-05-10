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

analysis = Analyse("dataset/Environment_Temperature_change.csv")

def viewDataset():
    st.header('Datasets used in this Analysis')
    with st.spinner("Loading Data ..."):
        st.dataframe(analysis.getDataframe())

def viewForm():

    st.plotly_chart(plot())

    title = st.text_input("Report Title")
    desc = st.text_area('Report Description')
    btn = st.button("Submit")

    if btn:
        report1 = Report(title = title, desc = desc, data = "")
        sess.add(report1)
        sess.commit()
        st.success('Report Saved')

def analyseTemperature():
    st.header('Average Temperature rise in Countries')
    selConl = st.selectbox(options = analysis.getCountries(), label="Which Country")
    data1 = analysis.country_df(selConl)
    with st.spinner('Loading Plot...'):
        st.plotly_chart(plotLine(data1, 'year', 'Meteorological year', title="Line Chart showing the fluctuation in temperature change"))

    selConb = st.selectbox(options = analysis.getCountries(), label="Which Country ")
    data2 = analysis.country_df(selConb)
    with st.spinner('Loading Plot...'):
        st.plotly_chart(plotBar(data2, 'year', 'Meteorological year'))

    selMon = st.selectbox(options = analysis.getMonths(), label="Which Month")
    countries = ['usa', 'india']
    
    selcountry = st.selectbox(options = countries, label="Which Country")
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
    titlesList = [ report.title for report in reports ]
    selReport = st.selectbox(options = titlesList, label= "Select Report")
    
    reportToView = sess.query(Report).filter_by(title = selReport).first()

    markdown = f"""
        ## {reportToView.title}
        ### {reportToView.desc}
        
    """

    st.markdown(markdown)



sidebar.header('Choose Your Option')
options = [ 'View Dataset', 'Analyse Temperature', 'View Report' ]
choice = sidebar.selectbox( options = options, label="Choose Action" )

if choice == options[0]:
    viewDataset()
elif choice == options[1]:
    analyseTemperature()
elif choice == options[2]:
    viewReport()