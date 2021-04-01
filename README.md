# nba_dashboard

This project is intented to scrape and format NBA data from [basketball-reference.com](https://www.basketball-reference.com/leagues/NBA_2021_games-january.html) then use that data to create a predictive model and deploy it through a dashboard that shows the upcoming games with supporting data.

## Features
Everytime ```main.py``` is executed, data is collected from the web, it performs feature engineering, then runs a Random Forest Classifier algorithm to make predictions of all the games.

## Screenshot Examples
![Dashboard Screenshot](Example/Dashboard.JPG)

## Tech / Libraries Used
* **Language(s):**
    * Python 3
* **Libraries:**
    * pandas==version = 1.2.3
    * numpy==version = 1.20.1
    * re==version = 2021.3.17
    * dash==version = 1.19.0
    * plotly==version = 4.14.3
    * scikit-learn==version = 0.24.1
    * lxml
    * selenium
