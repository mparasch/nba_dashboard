import pandas as pd
import re

years = range(2019, 2022) # input the start and end date+1 
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

df.to_csv(f'nba_data_{min(years)}_{max(years)}.csv')
print(f'Sucess! New file created in active directory: nba_data_{min(years)}_{max(years)}.csv')