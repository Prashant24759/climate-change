import plotly.graph_objects as go
import plotly.express as px


def plotBar(df, x, y,  title="default title", color_continuous_scale="rainbow"):
    fig = px.bar(df,
                 x=x,
                 y=y,
                 #  color=color,
                 color_continuous_scale=color_continuous_scale,
                 title=title)
    return fig


def plotGroupedBar(datapoints, names,  title="default title", xlabel="xlabel", ylabel='ylabel', color_continuous_scale="rainbow"):
    layout = go.Layout(title=title,
                       xaxis=dict(title=xlabel),
                       yaxis=dict(title=ylabel))

    fig = go.Figure(layout=layout)

    for point, name in zip(datapoints, names):
        fig.add_trace(go.Bar(x=point.index, y=point.values, name=name))

    return fig


def plotLine(df, x, y,  title="default title", color_continuous_scale="rainbow"):
    fig = px.line(df,
                  x=x,
                  y=y,
                  #  color=color,
                  #  color_continuous_scale=color_continuous_scale,
                  title=title)
    return fig


def plotChloropeth(datapoints, title="default title", xlabel="default xlabel", ylabel="default ylabel"):

    layout = go.Layout(title=title,
                       xaxis=dict(title=xlabel),
                       yaxis=dict(title=ylabel))

    fig = go.Figure({
        "type": 'choropleth',
        "locations": datapoints.index,
        "locationmode": 'country names',
        "z": datapoints.values},
        layout=layout)

    return fig


def plotPie(values,  labels, title="default title"):
    layout = go.Layout(title=title)
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Pie(labels=labels, values=values, title=title, textinfo='label+percent', hole=0.2,
                         marker=dict(colors=['#f7d468', '#74cb35'],
                                     line_color='Gray',
                                     line_width=1),
                         textfont={'color': '#000', 'size': 12},
                         textfont_size=12))
    return fig
