import pandas as pd
import re

def scrape_games(form = 'dataframe', startYear = 2015, endYear = 2021):
    years = range(startYear, endYear)
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

    df.dropna(subset=['Vis_Pts', 'Home_Pts'], inplace=True, axis=0)

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
    
    if form == 'dataframe':
        return df
    elif form == 'csv':
        df.to_csv(f'nba_data_{min(years)}_{max(years)}.csv')
        print(f'Sucess! New file created in active directory: nba_data_{min(years)}_{max(years)}.csv')

def format_by_team(df, team = 'All'):
    if team == 'All':
        df_total = pd.DataFrame()
        for i in df['Home_Team'].unique():
            df_vis = df.copy()[df['Vis_Team']==i]
            df_vis['Loc'] = 'Away'
            df_home = df.copy()[df['Home_Team']==i]
            df_home['Loc'] = 'Home'

            home_columns = ['Season', 'Date', 'Game_Day', 'Time_ET', 'Opp', 'Opp_Pts', 'Team', 'Team_Pts', 'OT', 'Attend', 
                        'Notes', 'Loc']
            vis_columns = ['Season', 'Date', 'Game_Day', 'Time_ET', 'Team', 'Team_Pts', 'Opp', 'Opp_Pts', 'OT', 'Attend', 
                            'Notes', 'Loc']

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