from itertools import groupby
import pandas as pd


class Analyse:

    def __init__(self, path):
        self.df = pd.read_csv(path, encoding="ISO-8859-1")
        # self.df = self.df.head(1000)
        if path.endswith('Environment_Temperature_change.csv'):
            self.cleanData1()

        self.years = list(range(1961, 2020))

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
        self.df.rename(columns={self.df.columns[-1] : 'disasters'}, inplace=True)
        return self.df.sort_values('Year')