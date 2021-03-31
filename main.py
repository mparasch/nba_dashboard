# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import nba_data as nba
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from datetime import date, timedelta
import datetime as dt
import odds_data

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

today = pd.Timestamp('today').replace(hour=0, minute=0, second=0, microsecond=0)

current_year = pd.datetime.now().year

start_year = current_year - 2

df_raw = nba.run_all(startYear=start_year, endYear=current_year)
df_raw = df_raw[df_raw['Date']>=today]
df_feat = nba.keep_features(df_raw)
df = nba.prediction(df_raw, df_feat)
df = df[df['Date']==pd.datetime.now().date()]

df['Rating'] = df['confidence'].apply(lambda x:
    '⭐⭐⭐⭐⭐' if x > 0.6234027304661728 else (
    '⭐⭐⭐⭐' if x > 0.5831375078444988 else (
    '⭐⭐⭐' if x > 0.5521258650846338 else (
    '⭐⭐' if x > 0.5246168930553068 else '⭐'
))))

df_odds = odds_data.scrape()

df = df.merge(df_odds, how='left', left_on='Winner_Prediction', right_on='Teams')
df.drop(columns='Teams', inplace=True)

df['Implied_Prob'] = df['Odds'].apply(lambda x: odds_data.implied_prob(x))

app = dash.Dash(__name__)

colors = {'background':'#1d3557',
           'header':'#a8dadc',
           'text':'#f1faee'}

header1 = {'textAlign':'center',
            'font-family':'helvetica',
            'color':colors['header'],
            'paddingTop': '25px',
            'marginTop': '0px',
            'marginLeft': '0px',
            'marginRight': '0px'}

header2 = {'textAlign':'center',
            'font-family':'helvetica',
            'color':colors['header']}

padding = {'marginLeft':'20px', 
            'marginRight':'20px'}

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(style = header1, children='NBA Dashboard'),
    html.H2(style = header2, children='Upcoming Predictions'),
    dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in df.columns], data=df.to_dict('records'),style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={'backgroundColor': 'rgb(230, 230, 230)',
                  'fontWeight': 'bold'},

    style_table={'maxHeight': '60ex',
                'overflowY': 'scroll',
                'width': '97%',
                'minWidth': '70%',
                'justify': 'center',
                'marginLeft': 'auto', 
                'marginRight': 'auto'
    }),
    html.H3(style={'backgroundColor': colors['background'], 'color' : colors['text'], 'font-family':'helvetica', 'marginLeft':'30px'}, children=['Accuracy:', html.Br(), '⭐⭐⭐⭐⭐ ~ 80%', html.Br(), '⭐⭐⭐⭐ ~ 71%', html.Br(), '⭐⭐⭐ ~ 65%', html.Br(), '⭐⭐ ~ 60%', html.Br(), '⭐ ~ 50%', html.Br(), '_'])
])

if __name__ == '__main__':
    app.run_server(debug=False)