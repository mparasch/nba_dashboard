import pandas as pd
import re
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def scrape_games(form = 'dataframe', startYear = 2015, endYear = 2021):
    years = range(startYear, endYear+1)
    months = ['december', 'january', 'february','march']
    columns = ['Date', 'Time_ET', 'Vis_Team', 'Vis_Pts', 'Home_Team', 'Home_Pts', 'Box', 'OT', 'Attend','Notes']

    df = pd.DataFrame()

    for year in years:
        for month in months:
            df_n = pd.read_html(f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html')[0]
            df_n.columns = columns
            df_n['Season'] = '{}-{}'.format(year-1, year)
            if df.empty:
                df = df_n
            else:
                df = df.append(df_n)



    def date_reformat(date):
        char_to_replace = {'Dec':'12','Jan':'01','Feb':'02','Mar':'03'}
        for key, value in char_to_replace.items():
            date = date.replace(key, value)
        l = re.split(', | ', date)
        dow = l[0]
        date = '/'.join(l[1:])
        return date, dow

    df['Game_Day'] = df['Date'].apply(lambda x: date_reformat(x)[1])
    df['Date'] = df['Date'].apply(lambda x: date_reformat(x)[0])

    df = df[['Season', 'Date', 'Game_Day', 'Time_ET', 'Vis_Team', 'Vis_Pts', 'Home_Team', 'Home_Pts', 'OT', 'Attend','Notes']]

    df['Date'] = pd.to_datetime(df['Date'])

    def concat3(x):
        return str(x[0]) + '_' + x[1] + '_vs_' + x[2]

    df['Matchup_ID'] = df[['Date', 'Home_Team', 'Vis_Team']].apply(concat3, axis=1)
    df['Matchup_ID'] = df['Matchup_ID'].astype(str)
    
    if form == 'dataframe':
        return df
    elif form == 'csv':
        df.to_csv(f'nba_data_{min(years)}_{max(years)}.csv')
        print(f'Sucess! New file created in active directory: nba_data_{min(years)}_{max(years)}.csv')

def format_by_team(df, team = 'All'):
    df = df.copy().drop('Matchup_ID', axis=1)
    if team == 'All':
        df_total = pd.DataFrame()
        for i in df['Home_Team'].unique():
            df_vis = df.copy()[df['Vis_Team']==i]
            df_vis['Loc'] = 'Away'
            df_home = df.copy()[df['Home_Team']==i]
            df_home['Loc'] = 'Home'

            home_columns = ['Season', 'Date', 'Game_Day', 'Time_ET', 'Opp', 'Opp_Pts', 'Team', 'Team_Pts', 'OT', 'Attend', 'Notes', 'Loc']
            vis_columns = ['Season', 'Date', 'Game_Day', 'Time_ET', 'Team', 'Team_Pts', 'Opp', 'Opp_Pts', 'OT', 'Attend', 'Notes', 'Loc']

            df_home.columns = home_columns
            df_vis.columns = vis_columns
            df_home = df_home[df_vis.columns]
            df_final = df_home.append(df_vis)
            
            if df_total.empty:
                df_total = df_final
            else:
                df_total = df_total.append(df_final)
        return df_total
    else:
        try:
            df_vis = df.copy()[df['Vis_Team']==team]
            df_vis['Loc'] = 'Away'
            df_home = df.copy()[df['Home_Team']==team]
            df_home['Loc'] = 'Home'

            home_columns = ['Season', 'Date', 'Game_Day', 'Time_ET', 'Opp', 'Opp_Pts', 'Team', 'Team_Pts', 'OT', 'Attend', 
                        'Notes', 'Loc']
            vis_columns = ['Season', 'Date', 'Game_Day', 'Time_ET', 'Team', 'Team_Pts', 'Opp', 'Opp_Pts', 'OT', 'Attend', 
                            'Notes', 'Loc']

            df_home.columns = home_columns
            df_vis.columns = vis_columns
            df_home = df_home[df_vis.columns]

            df_final = df_home.append(df_vis)
            return df_final
        except:
            print('Invalid Dataframe or Team value')

def feature_eng(df, n_roll=10):

    # Formats general features to be useful for predictive modeling
    def concat2(x):
        return str(x[0]) + '_' + x[1]

    def concat3(x):
        return str(x[0]) + '_' + x[1] + '_vs_' + x[2]
    
    df['Team_ID'] = df[['Date','Team']].apply(concat2, axis=1)
    df['Team_ID'] = df['Team_ID'].astype(str)

    df['Opp_ID'] = df[['Date','Opp']].apply(concat2, axis=1)
    df['Opp_ID'] = df['Opp_ID'].astype(str)

    df['Matchup_ID'] = df[['Date', 'Team', 'Opp']].apply(concat3, axis=1)
    df['Matchup_ID'] = df['Matchup_ID'].astype(str)

    df['Loc'].replace({'Home':1, 'Away':0}, inplace=True)

    def win_loss(x):
        if x[0] > x[1]:
            return 1
        elif x[0] < x[1]:
            return 0
    
    df['Outcome'] = df[['Team_Pts','Opp_Pts']].apply(win_loss, axis=1)

    # Creates Rolling totals for each feature
    df_teamR = pd.DataFrame()
    for team in df['Team'].unique():
        df1 = df.copy()[df['Team']==team]
        df1.sort_values(by='Date', inplace=True)
        df1['R_TeamPtsFor'] = df1['Team_Pts'].shift().rolling(n_roll).mean()
        df1['R_TeamWinPct'] = df1['Outcome'].shift().rolling(n_roll).mean()
        if df_teamR.empty:
            df_teamR = df1
        else:
            df_teamR = df_teamR.append(df1)

    df_opp = pd.DataFrame()
    for team in df['Opp'].unique():
        df1 = df.copy()[df['Opp']==team]
        df1.sort_values(by='Date', inplace=True)
        df1['R_OppPtsFor'] = df1['Team_Pts'].shift().rolling(n_roll).mean()
        df1['R_OppWinPct'] = df1['Outcome'].shift().rolling(n_roll).mean()
        df1 = df1[['Opp_ID', 'R_OppPtsFor', 'R_OppWinPct']]
        if df_opp.empty:
            df_opp = df1
        else:
            df_opp = df_opp.append(df1)

    df_teamR = df_teamR.merge(df_opp, left_on='Opp_ID', right_on='Opp_ID', how='left', suffixes=(None,'_'))

    # Adds in Season Averages
    df_season = df.groupby(by=['Season','Team']).agg({'Team_Pts':'mean','Opp_Pts':'mean', 'Outcome':'mean'}, 
                                                 as_index=False).reset_index()

    df_TeamAvg = pd.DataFrame()
    for season in df['Season'].unique():
        df1 = df_season[df_season['Season']==season][['Team','Team_Pts','Opp_Pts', 'Outcome']]
        df1.rename(columns={'Team_Pts': season + '_TeamPtsFor', 'Opp_Pts': season + '_TeamPtsAllowed', 
                            'Outcome':season + '_TeamWinPct'}, inplace=True)
        if df_TeamAvg.empty:
            df_TeamAvg = df1
        else:
            df_TeamAvg = df_TeamAvg.merge(df1, left_on='Team', right_on='Team', how='left')

    df_OppAvg = pd.DataFrame()
    for season in df['Season'].unique():
        df1 = df_season[df_season['Season']==season][['Team','Team_Pts','Opp_Pts', 'Outcome']]
        df1.rename(columns={'Team_Pts': season + '_OppPtsFor', 'Opp_Pts': season + '_OppPtsAllowed',
                        'Outcome':season + '_OppWinPct'}, inplace=True)
        if df_OppAvg.empty:
            df_OppAvg = df1
        else:
            df_OppAvg = df_OppAvg.merge(df1, left_on='Team', right_on='Team', how='left')
    
    df_full = df_teamR.merge(df_TeamAvg, left_on='Team', right_on='Team', how='left', suffixes=(None, "_"))
    df_full = df_full.merge(df_OppAvg, left_on='Opp', right_on='Team', how='left', suffixes=(None, "_"))

    return df_full

def predict_format(df_raw, df_feat):
    drop_cols = ['Season', 'Date', 'Game_Day', 'Time_ET', 'Team', 'Team_Pts', 'Opp', 'Opp_Pts', 'OT', 'Attend', 
                'Notes', 'Team_ID', 'Opp_ID', 'Team_']

    df_feat = df_feat.copy().drop(columns=drop_cols)

    df_feat['Matchup_ID'] = df_feat['Matchup_ID'].astype(str)
    df_raw['Matchup_ID'] = df_raw['Matchup_ID'].astype(str)

    df_new = df_raw.merge(df_feat, left_on='Matchup_ID', right_on='Matchup_ID', how='left', suffixes=(None,'_'))

    return df_new

def run_all(startYear = 2018, endYear = 2021, n_roll = 10):
    df_raw = scrape_games(startYear=startYear, endYear=endYear)
    df_team = format_by_team(df_raw)
    df_feat = feature_eng(df_team, n_roll=n_roll)
    df_final = predict_format(df_raw, df_feat)
    df_final.dropna(subset=['R_OppPtsFor', 'R_OppWinPct', 'R_TeamPtsFor', 'R_TeamWinPct'],
                    inplace=True, axis=0)
    return df_final

def keep_features(df):
    check = ['Outcome', 'Loc', 'R_', '_TeamWin', '_TeamPts', '_OppWin', '_OppPts']

    keep = []
    for col in df.columns:
        for i in check:
            if i in col and i not in keep:
                keep.append(col)

    df = df.copy()[keep]

    return df

def prediction(df_raw, df):
    clf = pickle.load(open("nbaPredict.pickle", "rb"))
    X = df[[col for col in df.columns if col!='Outcome']]
    
    clf.predict(X)
    proba = clf.predict_proba(X)
    predict = clf.predict(X)
    arr2 = np.hsplit(proba, 2)
    arr = np.stack((predict, arr2[0].flatten(), arr2[1].flatten()), axis=1)
    df_result = pd.DataFrame(arr, columns=['predict', '0', '1'])

    def greater(x):
        if x[0] > x[1]:
            return x[0]
        else:
            return x[1]

    df_result['confidence'] = df_result[['0','1']].apply(greater, axis=1)
    df_result.drop(columns=['0','1'], inplace=True)

    cols = ['Date','Game_Day', 'Time_ET', 'Home_Team', 'Vis_Team']
    df_raw = df_raw.copy()[cols]

    result = pd.concat([df_raw.reset_index(), df_result.reset_index()], axis=1)
    result.drop(columns='index', inplace=True)
    result.sort_values(by='confidence', ascending=False, inplace=True)

    def winner(x):
        if x[0]==1:
            return x[1]
        elif x[0]==0:
            return x[2]
    
    result['Winner_Prediction'] = result[['predict','Home_Team', 'Vis_Team']].apply(winner, axis=1)
    result.drop(columns='predict', inplace=True)

    def date_change(x):
        return x.date()
    
    result['Date'] = result['Date'].apply(lambda x: date_change(x))
    return result
    