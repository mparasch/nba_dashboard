import pandas as pd

df = pd.read_csv(r'nba_data_2016_2021.csv', index_col=0)

def format_by_team(df, team):
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

df1 = format_by_team(df, "All")