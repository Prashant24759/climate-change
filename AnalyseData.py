import pandas as pd

class Analyse:

    def __init__(self, path):
        self.df = pd.read_csv(path)

        self.years = list(range(1961, 2020))

    def cleanData(self):
        self.df.drop(['Months Code', 'Element Code', 'Unit','Area Code'], axis=1, inplace=True)
        df_years=self.df.columns[3:].values
        self.df.rename(columns=dict(list(zip(df_years,years))),inplace=True)
        self.df.rename(columns={'Area' : 'Country'}, inplace = True)
        self.df.set_index('Country', inplace = True)

    def getMaxTempChange(self, country):
        return self.df.groupby(self.df.index).max().loc[country, self.years].plot(kind='line')