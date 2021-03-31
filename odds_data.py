from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import pandas as pd

def scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver.minimize_window()
    driver.get("https://www.bovada.lv/sports/basketball/nba")

    try:
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        teams = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
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
            if len(i.text)>0:
                if i.text[0]!='(':
                    odds_list.append(i.text)

        print(team_list, odds_list)
        
        if len(odds_list)==len(team_list):
            data = {'Teams':team_list, 'Odds':odds_list}
        elif len(odds_list)<len(team_list):
            data = {'Teams':team_list[0:len(odds_list)], 'Odds':odds_list}

        df = pd.DataFrame(data)
        return df
    
    except:
        driver.quit()
        print('Error occured... Re-running Bovada scrape')
        scrape()
    
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