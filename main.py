import pandas as pd
import numpy as np
import nba_data as nba
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from datetime import date

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

today = pd.Timestamp('today')

app = dash.Dash(__name__)

colors = {'background':'#1d3557',
           'header':'#a8dadc',
           'text':'#f1faee'}

header1 = {'textAlign':'center',
            'font-family':'helvetica',
            'color':colors['header']}

header2 = {'textAlign':'center',
            'font-family':'helvetica',
            'color':colors['header']}

df_raw = nba.run_all(startYear=2019, endYear=2021)
df_raw = df_raw[df_raw['Date']>=today]
df_feat = nba.keep_features(df_raw)
df = nba.prediction(df_raw, df_feat)

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(style = header1, children='NBA Dashboard'),
    html.H2(style = header2, children='Upcoming Predictions'),
    dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in df.columns],
                         data=df.to_dict('records')),
    html.H1(style={'backgroundColor': colors['background']}, children=' \n \n \n \n')
])

if __name__ == '__main__':
    app.run_server(debug=True)