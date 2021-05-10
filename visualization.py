import plotly.graph_objects as go
import plotly.express as px

def plot():
    fig = go.Figure()

    fig.add_trace( go.Line( x = [i for i in range(10)] , y = [ i*i for i in range(10) ] ) )

    return fig

def plotBar(df, x, y,  title = "default title", color_continuous_scale="rainbow"):
    fig = px.bar(df,
             x=x,
             y=y,
            #  color=color,
             color_continuous_scale=color_continuous_scale,
             title=title)
    return fig

def plotLine(df, x, y,  title = "default title", color_continuous_scale="rainbow"):
    fig = px.line(df,
             x=x,
             y=y,
            #  color=color,
            #  color_continuous_scale=color_continuous_scale,
             title=title)
    return fig

# def continent_season_plot(season):
#     p = plt.figure(figsize=(10,10))
#     for con, c in list(zip(continents, colors)):
#         sns.regplot(data=con, x='year', y=season, fit_reg=True, lowess=True, label=con.index.name, 
#                     scatter_kws={'alpha':0.2}, ci=None, color=c, line_kws={'lw':2, 'alpha':0.75})
#     plt.ylabel('∆ °C', rotation=0)
#     plt.title(f'{season} ∆ Continental Temperatures')
#     plt.legend(loc='best', frameon=False)