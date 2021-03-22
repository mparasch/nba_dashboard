from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scrape():
    driver = webdriver.Firefox()
    driver.get("https://www.bovada.lv/sports/basketball/nba")

    try:
        teams = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "name"))
        )
        team_list = []

        for i in teams:
            if i.text !='L.A. Clippers':
                team_list.append(i.text)
            else:
                team_list.append('Los Angeles Clippers')

        odds = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "bet-price"))
        )

        odds_list = []

        for i in odds:
            if i.text[0]!='(':
                odds_list.append(i.text)

        data = {'Teams':team_list, 'Odds':odds_list}

        df = pd.DataFrame(data)
        return df

    finally:
        driver.quit()

def implied_prob(payout):
    payout = str(payout)
    if payout.upper()=='EVEN':
        return '50%'
    elif payout[0]=='-':
        payout = int(payout[1::])
        prob = int(payout/(payout + 100)*100)
        return str(prob) + '%'
    elif payout[0]=='+':
        payout = int(payout[1::])
        prob = int(100/(payout + 100)*100)
        return str(prob) + '%'
    else:
        return 'N/A'