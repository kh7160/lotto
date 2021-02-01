import requests
from bs4 import BeautifulSoup

import fund_parse

url = 'https://dhlottery.co.kr/common.do?method=main'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
# 7 num crawling

group = soup.select('.group .num span')
group = group[0].text

num = []
num.append(int(soup.find_all('span', {'class' : 'num al720_color1'})[0].text))
num.append(int(soup.find_all('span', {'class' : 'num al720_color2'})[0].text))
num.append(int(soup.find_all('span', {'class' : 'num al720_color3'})[0].text))
num.append(int(soup.find_all('span', {'class' : 'num al720_color4'})[0].text))
num.append(int(soup.find_all('span', {'class' : 'num al720_color5'})[0].text))
num.append(int(soup.find_all('span', {'class' : 'num al720_color6'})[0].text))

# mysql update
fund_parse.fund_update_group(group)
fund_parse.fund_update_number(num)