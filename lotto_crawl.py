import requests
from bs4 import BeautifulSoup
import lotto_parse

url = 'https://dhlottery.co.kr/common.do?method=main'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
# 7 num crawling
num = []
num.append(int(soup.find("span", id='drwtNo1').text))
num.append(int(soup.find("span", id='drwtNo2').text))
num.append(int(soup.find("span", id='drwtNo3').text))
num.append(int(soup.find("span", id='drwtNo4').text))
num.append(int(soup.find("span", id='drwtNo5').text))
num.append(int(soup.find("span", id='drwtNo6').text))
num.append(int(soup.find("span", id='bnusNo').text))

# mysql update
lotto_parse.update_number(num)