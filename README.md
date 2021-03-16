# nba_dashboard

This project is intented to scrape and format NBA data from [basketball-reference.com](https://www.basketball-reference.com/leagues/NBA_2021_games-january.html) then use that data to create a predictive model and deploy it through a dashboard that shows the upcoming games with supporting data.

## Features
### nba_data.py
It collects data about each game for the timeframe specified. The specific details collected are Date, Time, Visitor Team, Visitor Points, Home Team, Home Points, Attendance, Notes.

### main.py


## Screenshot Examples
![Dashboard Screenshot](Example/Dashboard.JPG)

## Tech / Libraries Used
* **Language(s):**
    * Python 3
* **Libraries:**
    * pandas
    * numpy
    * re
    * dash -- version = 1.19.0
    * plotly -- version = 4.14.3
    * sklearn -- version = 0.24.1

## Code Example

### Import
To leverage these functions from another python script, move the ```nba_data.py``` file into the same directory as your script.\
\
Simply import the file with the rest of your imports by using ```import nba_data```

### Functions

#### Data Collection
```nba_data.scrape_games(type=('csv','dataframe'), startYear, endYear)```
* **type:** Defines what output you would like for the data. Two options: 'csv' exports to .csv file in current directory and 'dataframe' returns a dataframe in your script.
* **startYear:** The earliest year that you want to collect data.
* **endYear:** The last year that you want to collect data.\
\
Example: ```nba_data.scrape_games('dataframe', 2015, 2021)``` returns a dataframe of all games from 2015 through 2021.

#### Data Formatting
This function reformats that data imported from ```nba_data.scrape_games()``` by duplicating each game and creating a record for the home team and another for the away team.\
```nba_data.format_by_team(df, team)```
* **df:** this paramater must be a dataframe that is produced from ```nba_data.scrape_games()```. Any other format will return errors.
* **team:** default = 'All' which returns .

Example: ```nba_data.format_by_team(df, team = 'Milwaukee Bucks')``` creates a dataframe for all of Bucks games in the dataframe. Alternatively, you can pass ```team = 'All'``` and it will iterate over all teams and append each team output to a single dataframe.

