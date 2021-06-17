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
st.image("logo.jpg")
sidebar = st.sidebar


@st.cache(suppress_st_warning=True)
def loadTempData():
    return Analyse("dataset/Environment_Temperature_change.csv")


# @st.cache(suppress_st_warning=True)
def loadDisasterData():
    return Analyse("dataset/natural-disaster-events.csv")


# @st.cache(suppress_st_warning=True)
def loadEconomicData():
    return Analyse("dataset/natural-disasters-loss.csv")


@st.cache(suppress_st_warning=True)
def loadFloodData():
    return Analyse("dataset/flood_damage.xls")


@st.cache(suppress_st_warning=True)
def loadSeaData():
    return Analyse("dataset/sea_levels.csv")


analysis = loadTempData()
disasterAnalysis = loadDisasterData()
seaAnalysis = loadSeaData()
floodAnalysis = loadFloodData()
EconomicAnalysis = loadEconomicData()


current_report = dict().fromkeys(
    ['title', 'desc', 'img_name', 'save_report'], "")

def overview():
    st.header('Global Warming And Climate Change')
    st.markdown('''
        ### *Climate change includes both global warming driven by human-induced emissions of greenhouse gases and the resulting large-scale shifts in weather patterns.*
    ''')
    st.image('climate.jpeg')

    st.markdown('''### Global warming is the increase of average world temperatures as a result of what is known as the greenhouse effect. As the greenhouse gases build up in the atmosphere the Earth gets hotter. This process is leading to a rapid change in climate, also known as climate change .
    ''')
    st.header('Project Introduction')
    st.markdown('''### In this project we have been to create models of how changes caused by heating should work their way through the entire system and appear in different areas, for example, Sea Level, Flood,Extreme Weather,Volcanic Activity etc .
    ''')
    st.image('global_warming.jpg')
    st.header('Objective')
    st.subheader(' Earth Observation :')
    st.markdown(''' Understanding and Predicting the global atmospheric and climate change .
    ''')
    st.subheader(' Climate Impact :')
    st.markdown('''   To increase the understanding of the atmosphere/ecosystem exchange of greenhouse gasses .
    ''')
    st.subheader('Temperature Analysis :')
    st.markdown('''  Specific analysis of the impact of selected climatic scenarios on Exchange of temperature . ''')
    st.header('Conclusion')
    st.markdown(''' ### The project will contribute to an improved understanding of the processes, and also use the knowledge gained to make an estimate of the contribution from the natural ecosystems to the emissions of greenhouse gasses .
    ''')
    st.markdown(''' ### Human-induced climate change has contributed to changing patterns of extreme weather across the globe, from longer and hotter heat waves to heavier rains. Extreme weather is on the rise, and the indications are that it will continue to increase, in both predictable and unpredictable ways.
    ''')


def generateReport():
    sidebar.header("Save Report")
    current_report['title'] = sidebar.text_input('Report Title')
    current_report['desc'] = sidebar.text_input('Report Description')
    current_report['img_name'] = sidebar.text_input('Image Name')
    current_report['save_report'] = sidebar.button("Save Report")


def save_report_form(fig):
    generateReport()
    if current_report['save_report']:
        with st.spinner("Saving Report..."):
            try:
                path = 'reports/'+current_report['img_name']+'.png'
                fig.write_image(path)
                report = Report(
                    title=current_report['title'], desc=current_report['desc'], img_name=path)
                sess.add(report)
                sess.commit()
                st.success('Report Saved')
            except Exception as e:
                st.error('Something went Wrong')
                print(e)


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
    selMon = st.selectbox(options=analysis.getMonths(), label=" Month")
    col1, col2 = st.beta_columns(2)
    
    fig1 = plotLine(analysis.country_df(selConl), 'year', 'Meteorological year',
                    title="Line Chart")
    with st.spinner('Loading Plot...'):
        col1.plotly_chart(fig1)
        btn = col1.checkbox(label="Save Report", key=1)
        if btn:
            save_report_form(fig1)
    fig2 = plotBar(analysis.country_df(selConl), 'year',
                   'Meteorological year', title="Bar Chart")
    with st.spinner('Loading Plot...'):
        col2.plotly_chart(fig2)
        btn = col2.checkbox(label="Save Report", key=2)
        if btn:
            save_report_form(fig2)

    st.text("Description here")

    st.markdown("---")
    
    
    selMon = st.selectbox(
        options=['spring', 'fall', 'winter', 'summer'], label=" Season")
    countries = ['USA', 'INDIA', 'UK', 'GERMANY', 'CANADA',
                 'AUSTRALIA', 'Ireland', 'Europe', 'Japan']

    selcountry = st.selectbox(options=countries, label=" Country")
    st.image(f'plotImages/{selcountry}_{selMon}.png')

    st.markdown('___')
    st.header('Average Temperature rise in seasons')
    st.image('plotImages/temp_shift.png')
    st.markdown('___')

    st.header('Comparing the World Temperature with respect to years')
    st.image('plotImages/world_line.png')
    st.markdown('___')

    st.header('Comparing the Country Temperatures with respect to years')
    st.image('plotImages/world_line.png')
    st.markdown('___')

    st.header('Continental temperature rise in various seasons')
    st.image('plotImages/season_continent.png')
    st.markdown('___')

def analyseFloods():
    st.header('Flood Damage India')
    fig = plotLine(floodAnalysis.getDataframe(),
                   'Year', 'Area affected-India', title="Total Area Damaged in India")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=1)
    if btn:
        save_report_form(fig)
    st.text('''Discription : In this above chart we can see that how much area affected by Flood in India
            In 1978 Maximum area affected by Flood in India''')
    st.markdown("___")
    fig = plotLine(floodAnalysis.getDataframe(),
                   'Year', 'Population affected-India', title="Total Population Affected in India")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=2)
    if btn:
        save_report_form(fig)
    st.text('''Discription : In this above chart we can see that how much Population affected by Flood in India
            In 1978 Maximum Population affected by Flood in India''')
    st.markdown("___")
    fig = plotLine(floodAnalysis.getDataframe(),
                   'Year', 'Human lost no.-India', title="Total Humans loss in India")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=3)
    if btn:
        save_report_form(fig)
    st.text('''Discription : In this above chart we can see that how many human loss their lives during the Flood
      in India. In 1977 approximately 11.361K human loss their lives by Flood in India''')
    st.markdown("___")
    fig = plotLine(floodAnalysis.getDataframe(),
                   'Year', 'Damage C.area-Bihar', title="Total Crop Affected in Bihar")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=4)
    if btn:
        save_report_form(fig)
    st.text('''Discription : In this above chart we can see that how much crops damage by Flood in Bihar
            In 1987 Maximum crops damage by Flood in Bihar ''')
    st.markdown("___")
    fig = plotLine(floodAnalysis.getDataframe(),
                   'Year', 'Total damage crops,Houses & Public utilities in Rs.crore', title="Total damage in Bihar")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=5)
    if btn:
        save_report_form(fig)
    st.text('''Discription : In this above chart we can see that total damage by Flood in Bihar
             In 2004  Maximum damage include crops,houses, public utilities 
             approximately 2310.647 crore in Bihar''')
    st.markdown("___")
    fig = plotGroupedBar(floodAnalysis.getAreaData(), ('India', 'Bihar', 'Uttar Pradesh', 'Madhya Pradesh'),
                         xlabel="Year", ylabel="No. of Area Damage", title="Comparison of Crops Area damaged")

    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=6)
    if btn:

        save_report_form(fig)
    st.text('''Description : In this above chart we are comparing crops damage by flood in Bihar,Uttar Pradesh
              Madhya Pradesh.In 1979 Uttar Prasdesh faced the maximum damage due to flood
              In 1987 Bihar faced the maximum damage due to flood 
              In 2013 Madhya Prasdesh faced the maximum damage due to flood''')
    st.markdown("___")

    fig = plotGroupedBar(floodAnalysis.getPopulationData(), ('India', 'Bihar', 'Uttar Pradesh', 'Madhya Pradesh'),
                         xlabel="Year", ylabel="Total no. of population", title="Comparison of Population Affected")

    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=7)
    if btn:
        save_report_form(fig)
    st.text('''Description :In this above chart we are comparing population affected by flood in Bihar,Uttar Pradesh
              Madhya Pradesh.In 1980 maximum population affected by flood in Uttar Pradesh
              In 2004 maximum population affected by flood in Bihar 
              In 2014 maximum population affected by flood in Madhya Pradesh''')
    st.markdown("___")
    fig = plotGroupedBar(floodAnalysis.getHumanData(), ('India', 'Bihar', 'Uttar Pradesh', 'Madhya Pradesh'),
                         xlabel="Year", ylabel="Total no. of Humans", title="Comparison of Human Life Lost in Flood")

    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=8)
    if btn:
        save_report_form(fig)
    st.text('''Description :In this above chart we are comparing human life lost during flood in Bihar,Uttar Pradesh
              Madhya Pradesh.In 1998 maximum human lost their lives by flood in Uttar Pradesh 
              In 2007 maximum human lost their lives by flood in Bihar 
              In 2014 maximum human lost their lives  by flood in Madhya Pradesh''')
    st.markdown("___")
    fig = plotLine(floodAnalysis.getDataframe(),
                   'Year', 'Damage to Crops - Value in Rs.Crore - Uttar Pradesh', title="Total crops Affected in Uttar Pradesh")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=9)
    if btn:
        save_report_form(fig)
    st.text('''Discription : In this above chart we can see that how much crops damage by Flood in Uttar Pradesh
            In 1985 Maximum crops damage by Flood in Uttar Pradesh ''')
    st.markdown("___")
    
    fig = plotLine(floodAnalysis.getDataframe(),
                   'Year', 'Total damages Crops, Houses & Public utilities in Rs.Crore (col.6+8+11) - Uttar Pradesh', title="Total Damage in Uttar Pradesh")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=10)
    if btn:
        save_report_form(fig)
    st.text('''Discription : In this above chart we can see that total damage by Flood in Uttar Pradesh
             In 2001  Maximum damage include crops,houses, public utilities 
             approximately 3315.425 crore in Bihar''')
    st.markdown("___")

    fig = plotLine(floodAnalysis.getDataframe(),
                   'Year', 'Total damages Crops, Houses & Public utilities in Rs.Crore (col.6+8+11) - Madhya Pradesh', title="Total Damage in Madhya Pradesh")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=11)
    if btn:
        save_report_form(fig)
    st.text('''Discription : In this above chart we can see that total damage by Flood in Madhya Pradesh
             In 2014  Maximum damage include crops,houses, public utilities 
             approximately 464.06 crore in Madhya Pradesh''')
    st.markdown("___")


def analyseDisasters():

    st.markdown("#")
    st.header('Analysis of Natural Disasters')
    st.markdown('---')
    
    fig = plotBar(disasterAnalysis.getDisasterType(), 'Entity', 'Number of reported natural disasters (reported disasters)',
                  title="Types of Natural Disasters")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=1)
    if btn:
        save_report_form(fig)
    st.text("Discription : In the above chart we can see that type of Natural Disaster")
    st.markdown("___")
    fig = plotPie(disasterAnalysis.getDisasterCount(
    ).values, disasterAnalysis.getDisasterCount().index, title="No. of Disasters")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=2)
    if btn:
        save_report_form(fig)
    st.markdown("___")
    fig = plotLine(disasterAnalysis.getDisasterByYear(), 'Year', 'disasters',
                   title='Disasters per Year')
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=3)
    if btn:
        save_report_form(fig)
    st.text("Discription : In this above chart Number of Disaster per year increases.")
    st.text(" In 2005 maximum number of Disaster per year Occure")
    st.markdown("___")

    fig = plotLine(disasterAnalysis.getDroughtByYear(),
                   'Year', 'Drought', title="Drought Per Year")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=4)
    if btn:
        save_report_form(fig)
    st.text(''' Discription :  In this above chart Number of Drought per year increases. 
                In 2005 maximum number of Drought.
        ''')
    st.markdown("___")
    fig = plotLine(disasterAnalysis.getEarthquakeByYear(),
                   'Year', 'Earthquake', title="Earthquake Per Year")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=5)
    if btn:
        save_report_form(fig)
    st.text(''' Discription :  In this above chart Number of Earthquake per year increases. 
                In 2005 maximum number of Earthquake.''')
    st.markdown("___")
    fig = plotLine(disasterAnalysis.getWildfireByYear(), 'Year',
                   'Wildfire', title="Wildfire Per Year")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=6)
    if btn:
        save_report_form(fig)
    st.text(''' Discription :  In this above chart Number of WildFire per year increases. 
                In 2005 maximum number of WildFire.''')
    st.markdown("___")
    fig = plotLine(disasterAnalysis.getVolcanicActivityByYear(),'Year','Volcanic activity',title="Volcanic Activity Per Year")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=7)
    if btn:
        save_report_form(fig)
    st.text(''' Discription :  In this above chart Number of Volcanic Activity per year increases. 
                In 2005 maximum number of Volcanic Activity.''')   
    st.markdown("___")
    fig = plotLine(disasterAnalysis.getLandslideByYear(),'Year','Landslide',title="Landslide Per Year")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=8)
    if btn:
        save_report_form(fig)
    st.text(''' Discription :  In this above chart Number of Landslide per year increases. 
                In 2005 maximum number of Landslide.''') 
    st.markdown("___")
    fig = plotLine(disasterAnalysis.getExtremeWeatherByYear(),'Year','Extreme weather',title="Extreme Weather Per Year")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=9)
    if btn:
        save_report_form(fig)
    st.text(''' Discription :  In this above chart Number of Extreme Weather per year increases. 
                In 2005 maximum number of Extreme Weather.''') 
    st.markdown("___")

def analyseSeaLevel():
    st.header('Sea Levels')

    data = seaAnalysis.getDataframe()
    fig = plotLine(seaAnalysis.getDataframe(), 'Time', 'GMSL',
                   title="Sea Level Rise in by months of Years")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=1)
    if btn:
        save_report_form(fig)
    st.text("Discription :")
    st.markdown("___")

    fig = plotBar(seaAnalysis.getDataframe(), 'Time', 'GMSL',
                  title="Sea Level Rise in by months of Years")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=2)
    if btn:
        save_report_form(fig)
    st.text("Discription :")
    st.markdown("___")

    fig = plotBar(seaAnalysis.getAvgSeaLevelRise(),
                  'Year', 'GMSL', title="Average Sea Level Rise Every Year")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=3)
    if btn:
        save_report_form(fig)
    st.text("Discription :")
    st.markdown("___")

    fig = plotBar(seaAnalysis.getMinSeaLevelRise(),
                  'Year', 'GMSL', title="Minimum Sea Level Rise Every Year")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=4)
    if btn:
        save_report_form(fig)
    st.text("Discription :")
    st.markdown("___")

    fig = plotBar(seaAnalysis.getMaxSeaLevelRise(),
                  'Year', 'GMSL', title="Maximum Sea Level Rise Every Year")
    st.plotly_chart(fig)
    btn = st.checkbox(label="Save Report", key=5)
    if btn:
        save_report_form(fig)
    st.text("Discription :")
    st.markdown("___")


def ViewReport():
    reports = sess.query(Report).all()
    titleslist = [report.title for report in reports]
    selReport = st.selectbox(options=titleslist, label="Select Report")

    reportToView = sess.query(Report).filter_by(title=selReport).first()
    # st.header(reportToView.title)
    # st.text(report)

    markdown = f"""
        ## Title
        ### {reportToView.title}
        ## Description
        #### {reportToView.desc}
    """
    st.markdown(markdown)

    st.image(reportToView.img_name)


sidebar.header('Choose Your Option')
options = ['Project Overview', 'View Dataset', 'Analyse Climate', 'Analyse Floods',
           'Analyse other Disasters', 'Analyse Sea Level', 'View Report']
choice = sidebar.selectbox(options=options, label="Choose Action")

if choice == options[0]:
    overview()
elif choice == options[1]:
    viewDataset()
elif choice == options[2]:
    analyseTemperature()
elif choice == options[3]:
    analyseFloods()
elif choice == options[4]:
    analyseDisasters()
elif choice == options[5]:
    analyseSeaLevel()
elif choice == options[6]:
    ViewReport()
