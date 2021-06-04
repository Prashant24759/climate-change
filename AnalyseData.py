from itertools import groupby
import pandas as pd


class Analyse:

    def __init__(self, path):
        if path.endswith('csv'):
            self.df = pd.read_csv(path, encoding="ISO-8859-1")
        if path.endswith('xls'):
            self.df = pd.read_excel(path)
            self.df = self.df[:-4]
        # self.df = self.df.head(1000)
        if path.endswith('Environment_Temperature_change.csv'):
            self.cleanData1()
        elif path.endswith('flood_damage.xls'):
            self.cleanFloodData()
        elif path.endswith('sea_levels.csv'):
            self.cleanSeaData()

        self.years = list(range(1961, 2020))

        print('init run')

    def cleanFloodData(self):
        self.df.rename(columns={'Sl.No\n-India': 'India', 'Area affected in m.ha. - India': 'Area affected-India', 'Population affected in million - India': 'Population affected-India', 'Damage to Crops - Area in m. ha. - India': 'Damage C.area-India', 'Damage to Crops - Value in Rs.Crore - India': 'Damage C.value-India', 'Damage to Houses - Nos. - India': 'Damage H.no.-India', 'Damage to Houses - Value in Rs.Crore - India': 'Damage H.value-India', 'Cattle Lost Nos. - India': 'Cattle lost-India', 'Human live Lost Nos. - India': 'Human lost no.-India', 'Area affected in m.ha. - Bihar': 'Area affected-Bihar',
                                'Population affected in million - Bihar': 'Population affected-Bihar', 'Damage to Crops - Area in m. ha. - Bihar': 'Damage C.area-Bihar', 'Damage to Crops - Value in Rs.Crore - Bihar': 'Damage C.value-Bihar', 'Damage to Houses - Nos. - Bihar': 'Damage H.no.-Bihar', 'Damage to Houses - Value in Rs.Crore - Bihar': 'Damage H.value-Bihar', 'Human live Lost Nos. - Bihar': 'Human lost no.-Bihar', 'Damage to Public Utilities in Rs.Crore - Bihar': 'Damage public utilities-Bihar', 'Total damages Crops, Houses & Public utilities in Rs.Crore (col.6+8+11) - Bihar': 'Total damage crops,Houses & Public utilities in Rs.crore'}, inplace=True)

    def cleanSeaData(self):
        self.df['Year'] = pd.DatetimeIndex(self.df['Time']).year

    def getCountries(self):
        return self.df.area.unique()

    def getMonths(self):
        return self.df.months.unique()

    def cleanData1(self):
        # self.df.drop(['Months Code', 'Element Code', 'Unit','Area Code'], axis=1, inplace=True)
        # df_years=self.df.columns[3:].values
        # self.df.rename(columns=dict(list(zip(df_years,years))),inplace=True)
        # self.df.rename(columns={'Area' : 'Country'}, inplace = True)
        # self.df.set_index('Country', inplace = True)

        self.df.columns = self.df.columns.str.lower()
        self.df.columns = self.df.columns.str.replace('y', '')
        self.df.drop(columns=['area code', 'element code',
                              'months code', 'unit'], inplace=True)

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        seasons = ['Winter', 'Spring', 'Summer', 'Fall']

        seasons_replace = {'Dec\x96Jan\x96Feb': 'Winter', 'Mar\x96Apr\x96May': 'Spring',
                           'Jun\x96Jul\x96Aug': 'Summer', 'Sep\x96Oct\x96Nov': 'Fall', }
        self.df.replace(seasons_replace, inplace=True)

    def getMaxTempChange(self, country):
        return self.df.groupby(self.df.index).max().loc[country, self.years].plot(kind='line')

    def country_df(self, country):
        dfn = self.df[(self.df['element'] == 'Temperature change')
                      & (self.df['area'] == country)]
        dfn = dfn.set_index('months').transpose()[2:]
        dfn['year'] = dfn.index
        dfn.reset_index(drop=True, inplace=True)
        dfn.index.names = [country]
        dfn = dfn.astype('float')
        return dfn

    def getDataframe(self):
        return self.df

    def seasons_df(self, country):
        dfn = self.df[(self.df['element'] == 'Temperature change')
                      & (self.df['area'] == country)]
        dfn.rename(columns={'months': 'seasons'}, inplace=True)
        dfn = dfn.set_index('seasons').transpose()[2:]
        dfn['year'] = dfn.index
        dfn.drop(columns=months, inplace=True)
        dfn.reset_index(drop=True, inplace=True)
        dfn.index.names = [country]
        dfn = dfn.astype('float')
        return dfn

    def getYearTemperature(self, year):
        return self.df.set_index('area')[year]

    # def continent_season_plot(season, axes=None, subplot=False):
    #     if subplot == False:
    #         p = plt.figure(figsize=(10,10))
    #     for con, c in list(zip(continents, colors)):
    #         sns.regplot(data=con, x='year', y=season, fit_reg=True, lowess=True, label=con.index.name,
    #                     scatter_kws={'alpha':0.2}, ci=None, color=c, line_kws={'lw':2, 'alpha':0.75})
    #     if subplot == False:
    #         plt.ylabel('∆ °C', rotation=0)
    #         plt.title(f'{season} ∆ Continental Temperatures')
    #         plt.legend(loc='best', frameon=False)
    #     else:
    #         axes.set_ylabel('∆ °C', rotation=0)
    #         axes.set_title(f'{season} ∆ Continental Temperatures')
        # axes.legend(loc='upper left', frameon=True)

    def getDisasterType(self):
        return self.df.groupby('Entity', as_index=False).count()

    def getDisasterCount(self):
        return self.df.groupby('Entity').count()['Year']

    def getDisasterByYear(self):
        self.df.rename(
            columns={self.df.columns[-1]: 'disasters'}, inplace=True)
        return self.df.sort_values('Year')
    
    
    def getDroughtByYear(self):
        self.df.rename(
            columns={self.df.columns[-1]: 'Drought'}, inplace=True)
        return self.df.sort_values('Year')        

    def getEarthquakeByYear(self):
        self.df.rename(
            columns={self.df.columns[-1]: 'Earthquake'}, inplace=True)
        return self.df.sort_values('Year')

    def getWildfireByYear():
        self.df.rename(
            columns={self.df.columns[-1]: 'Wildfire'}, inplace=True)
        return self.df.sort_values('Year')
          
        
    def getAvgSeaLevelRise(self):
        return self.df.groupby('Year', as_index=False).mean()

    def getMinSeaLevelRise(self):
        return self.df.groupby('Year', as_index=False).min()

    def getMaxSeaLevelRise(self):
        return self.df.groupby('Year', as_index=False).max()

    def getEconomicLossByYear():
         return self.df.groupby('Total economic damage from natural disasters', as_index=False)

    def getAreaData(self):
        self.dfa = self.df.set_index('Year')
        return (
            self.dfa['Area affected-India'],
            self.dfa['Damage C.area-Bihar'],
            self.dfa['Damage to Crops - Area in m. ha. - Uttar Pradesh'],
            self.dfa['Damage to Crops - Area in m. ha. - Madhya Pradesh']
        )

    def getPopulationData(self):
        self.dfa = self.df.set_index('Year')
        return (
            self.dfa[ 'Population affected-India'],
            self.dfa['Population affected-Bihar'],
            self.dfa['Population affected in million - Uttar Pradesh'],
            self.dfa[ 'Population affected in million - Madhya Pradesh']
        )

    def getHumanData(self):
        self.dfa = self.df.set_index('Year')
        return(
            self.dfa['Human lost no.-India'],
            self.dfa['Human lost no.-Bihar'],
            self.dfa['Human live Lost Nos. - Uttar Pradesh'],
            self.dfa['Human live Lost Nos. - Madhya Pradesh']
        )    