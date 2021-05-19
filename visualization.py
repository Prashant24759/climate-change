import plotly.graph_objects as go
import plotly.express as px


def plot():
    fig = go.Figure()

    fig.add_trace(go.Line(x=[i for i in range(10)],
                          y=[i*i for i in range(10)]))

    return fig


def plotBar(df, x, y,  title="default title", color_continuous_scale="rainbow"):
    fig = px.bar(df,
                 x=x,
                 y=y,
                 #  color=color,
                 color_continuous_scale=color_continuous_scale,
                 title=title)
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
