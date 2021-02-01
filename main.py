from selenium import webdriver
import time
import lotto_parse
import os
import requests
import json
from datetime import datetime
from datetime import timedelta

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

driver.get('https://www.dhlottery.co.kr/user.do?method=login&returnUrl=')
driver.maximize_window()

# login
driver.find_element_by_xpath('/html/body/div[3]/section/div/div[2]/div/form/div/div[1]/fieldset/div[1]/input[1]').send_keys('kh7160')
driver.find_element_by_xpath('/html/body/div[3]/section/div/div[2]/div/form/div/div[1]/fieldset/div[1]/input[2]').send_keys('a!4862753')
driver.find_element_by_xpath('/html/body/div[3]/section/div/div[2]/div/form/div/div[1]/fieldset/div[1]/a').click()

time.sleep(3) # delay for pop up window

window_lst = driver.window_handles # close pop up window
for window in window_lst:
    if window != window_lst[0]: # except main window
        driver.switch_to.window(window)
        driver.close()
driver.switch_to.window(window_lst[0]) # to switch main page

money = driver.find_element_by_xpath('/html/body/div[1]/header/div[2]/div[2]/form/div/ul[1]/li/a[1]/strong').text # 잔금 확인
if money == '0원':
    print('돈이 없습니다. 충전이 필요합니다.')
    # exit(-1)

choice_num = lotto_parse.get_number()

driver.execute_script("window.open('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40');") # lotto 구매 프로그램 실행

time.sleep(7)

url = 'https://ol.dhlottery.co.kr/olotto/game/execBuy.do'
param = []
alpha = ['A', 'B', 'C', 'D', 'E']
# alpha = ['A'] # 수작업 용도
for i in range(len(choice_num)):
    choice_num[i].sort()
    param.append({"arrGameChoiceNum":f"{choice_num[i][0]},{choice_num[i][1]},{choice_num[i][2]},{choice_num[i][3]},{choice_num[i][4]},{choice_num[i][5]}","genType":"1","alpabet":f"{alpha[i]}"})

# today = datetime.now().strftime('%Y/%m/%d')
# today_after_year = datetime.now().strftime('%Y/%m/%d') + timedelta()
# print(today, today_after_year)

data = {
    'round': 947,
    # 'direct': '172.17.20.51',
    'nBuyAmount': 5000,
    'param': param,
    # 'ROUND_DRAW_DATE': '2021/01/16',
    # 'WAMT_PAY_TLMT_END_DT': '2022/01/17',
    'gameCnt': 5
}

# my data
# {   "round": 946
#     , "direct": "172.17.20.51"
#     , "nBuyAmount": 5000
#     , "param": [{"arrGameChoiceNum": "6,13,15,24,29,41", "genType": "1", "alpabet": "A"}, {"arrGameChoiceNum": "1,9,15,17,29,44", "genType": "1", "alpabet": "B"}, {"arrGameChoiceNum": "4,19,24,36,41,43", "genType": "1", "alpabet": "C"}, {"arrGameChoiceNum": "5,12,13,19,24,31", "genType": "1", "alpabet": "D"}, {"arrGameChoiceNum": "6,14,18,24,32,43", "genType": "1", "alpabet": "E"}]
#     , "ROUND_DRAW_DATE": "2021/01/16"
#     , "WAMT_PAY_TLMT_END_DT": "2022/01/17"
#     , "gameCnt": 5}

# real data
# round: 946
# direct: 172.17.20.51
# nBuyAmount: 3000
# param: [{"arrGameChoiceNum":"6,13,15,24,29,41","genType":"1","alpabet":"A"},{"arrGameChoiceNum":"1,9,15,17,29,44","genType":"1","alpabet":"B"},{"arrGameChoiceNum":"4,19,24,36,41,43","genType":"1","alpabet":"C"}]
# ROUND_DRAW_DATE: 2021/01/16
# WAMT_PAY_TLMT_END_DT: 2022/01/17
# gameCnt: 3

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://ol.dhlottery.co.kr/olotto/game/game645.do',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

s = requests.session()
for cookie in driver.get_cookies():
    c = {cookie['name'] : cookie['value']}
    s.cookies.update(c)

json_data = json.dumps(data)
print(json_data)
resp = s.post(url, data=json_data, headers = headers)
time.sleep(3) # delay for pop up window
print(resp.text)

driver.quit()
os.system("pkill chromedriver")

# https://ol.dhlottery.co.kr/olotto/game/egovUserReadySocket.json
# {"direct_yn":"N","ready_ip":"172.17.20.51","ready_time":"0","ready_cnt":"0"}

