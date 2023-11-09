import dash
from dash import Dash,dcc,html,Input,Output
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

TA = pd.read_excel("Tasa Activa Excel.xlsx")
TA
IN = pd.read_excel("Inflación Excel.xlsx")
IN
CB = pd.read_excel("Crédito Excel.xlsx")
CB

#construir dashboard
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.title="Dashboard"

app1=Dash(__name__)
server=app1.server

app1.layout=html.Div([
    dcc.Graph(id="graph"),
    html.P("Año:"),
    dcc.Dropdown(id="names",
                options=[1996, 1997, 1998, 1999, 2000, 2001, 2002, 
                         2003, 2004, 2005, 2006, 2007, 2008, 2009, 
                         2010, 2011, 2012, 2013, 2014, 2015, 2016, 
                         2017, 2018, 2019, 2020, 2021, 2022

],
                value=2022,clearable=False),
    
    #tabla
    html.Div(html.Div(id="table-container"),style={'marginBottom':'15px','marginTop':
                                                 "10px"}),

])

#establecer función callback para que actualice la gráfica según mi selección en dropdown
@app1.callback(
    [Output("graph","figure"),
    Output("table-container","children")],
    Input("names","value"))
def generate_chart(names):
    df = TA
    fig = px.line(df, x="Año/Mes", y=names, title=f"Tasas Activas para {names}",markers=True)
    fig.update_xaxes(title_text="Mes", title_font=dict(size=14, color="white"))  # Cambia el título y el color del eje X
    fig.update_yaxes(title_font=dict(size=14, color="white"))  # Cambia el título y el color del eje Y
    fig.update_xaxes(tickangle=55)
    fig.update_layout(
    plot_bgcolor="black",  # Cambia el fondo de la gráfica
    paper_bgcolor="black",  # Cambia el fondo del área del gráfico
    font=dict(family="Arial", size=14, color="white"),  # Cambia la fuente y el tamaño del texto
    title_font=dict(size=18, color="white"))
    fig.update_traces(marker_color="blue")
    fig.update_traces(marker=dict(color="white"))  # Cambia el color de los marcadores
    fig.update_traces(line=dict(width=3))  # Aumenta el ancho de las líneas
    fig.update_traces(marker=dict(size=5, line=dict(width=2, color="white")))  # Cambia el tamaño y el borde de los marcadores
    
    return (fig,dash_table.DataTable(columns=[{"name":i,"id":i} for i in TA],
                               data=TA.to_dict("records"),
                               export_format="csv",#para guardar como csv
                               fill_width=True,
                               style_header={'backgroundColor':'black',
                                            'color':'white'},
                               ))

app1.run_server(debug=False,host="0.0.0.0",port=1001)

app2=Dash(__name__)
server=app2.server

app2.layout=html.Div([
    dcc.Graph(id="graph"),
    html.P("Año:"),
    dcc.Dropdown(id="names",
                options=[1996, 1997, 1998, 1999, 2000, 2001, 2002, 
                         2003, 2004, 2005, 2006, 2007, 2008, 2009, 
                         2010, 2011, 2012, 2013, 2014, 2015, 2016, 
                         2017, 2018, 2019, 2020, 2021, 2022

],
                value=2022,clearable=False),

])

#establecer función callback para que actualice la gráfica según mi selección en dropdown
@app2.callback(
    Output("graph","figure"),
    Input("names","value"))
def generate_chart(names):
    df = IN
    fig = px.bar(df, x="Periodo", y=names, title=f"Inflación para {names}")
    fig.update_xaxes(title_text="Mes", title_font=dict(size=14, color="white"))  # Cambia el título y el color del eje X
    fig.update_yaxes(title_font=dict(size=14, color="white"))  # Cambia el título y el color del eje Y
    fig.update_xaxes(tickangle=55)
    fig.update_layout(
    plot_bgcolor="black",  # Cambia el fondo de la gráfica
    paper_bgcolor="black",  # Cambia el fondo del área del gráfico
    font=dict(family="Arial", size=14, color="white"),  # Cambia la fuente y el tamaño del texto
    title_font=dict(size=18, color="white"))
    fig.update_traces(marker_line=dict(width=2, color="white"))
    fig.update_traces(text=df[names], textposition="outside")
    fig.update_yaxes(range=[0, df[names].max() + 1.5])  # Personalizar los límites del eje Y
    fig.update_traces(marker_color="blue")
    return fig

app2.run_server(debug=False,host="0.0.0.0",port=10002)

app3 = Dash(__name__)
server=app3.server

app3.layout = html.Div([
    dcc.Graph(id="pie-chart"),
    html.P("Año:"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{'label': str(year), 'value': year} for year in CB['AÑOS']],
        value=2022,
        clearable=False
    ),
])

@app3.callback(
    Output("pie-chart", "figure"),
    Input("year-dropdown", "value"))
def generate_pie_chart(selected_year):
    df = CB[CB['AÑOS'] == selected_year]
    labels = ["Sector Público", "Sector Privado"]
    values = [df["Sector Público"].values[0], df["Sector Privado"].values[0]]
    fig = px.pie(names=labels, values=values, title=f"Proporción de crédito para {selected_year}")
    fig.update_traces(textinfo="percent")  # No muestra los nombres en el pie
    fig.update_traces(marker=dict(colors=['white', 'blue']))
    fig.update_layout(
        plot_bgcolor="black",  # Cambia el fondo del gráfico
        paper_bgcolor="black",  # Cambia el fondo del área del gráfico
        font=dict(family="Arial", size=14, color="white"),  # Cambia la fuente y el tamaño del texto
        title_font=dict(size=18, color="white")
    )

    return fig


if __name__ == '__main__':
    app3.run_server(debug=False,host="0.0.0.0",port=1003)
