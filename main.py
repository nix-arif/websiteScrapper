import requests
import random
from bs4 import BeautifulSoup as bs
import traceback
# import pandas as pd

def get_free_proxies():
  url = 'https://free-proxy-list.net/'
  soup = bs(requests.get(url).content, 'html.parser')

  proxies = []
  div_table = soup.find_all('div', class_= 'fpl-list')

  

  ths = []
  tds = []
  for div in div_table:
    ths = div.find_all('th')
  
  ths_text = []
  
  for th in ths:
    ths_text.append(th.text)

  datas = []

  for div in div_table:
    rows = div.find_all('tr')
    row_data = []
    for row in rows[1:]:
      data = row.find_all('td')
      row_data = [each_row.text for each_row in data]
      datas.append(row_data)
  
  proxies = [str(each_ip[0]) + ":" + str(each_ip[1]) for each_ip in datas]
  
  # print(datas[0:5])
  # df = pd.DataFrame(datas)
  # df.columns = ths_text
  # print(df.head())
  
  return proxies
  

url = 'http://httpbin.org/ip'
all_a_tag = []

proxies = get_free_proxies()

def webRequest(proxy):
  webUrl = 'https://www.jakelonline.com/main'
  try:
    # soup = bs(requests.get(webUrl).content, 'html.parser', proxies={"http": proxy, "https": proxy})
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    webHTML = requests.get(webUrl, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
    
    if webHTML.status_code == 200:
      soup = bs(webHTML.content, 'html.parser')
      all_a_tag = soup.find_all('a')
      return webHTML.status_code
  except requests.exceptions.ConnectTimeout:
    print("Web Time out")
  except requests.exceptions.HTTPError as e:
    print('Web HTTP Error')
  except requests.exceptions.ConnectionError:
    print('Web Connection Error')
  except:
    print('Web Other error')
  
  


for i in range(len(proxies)):
  proxy = proxies[i]
  # print('Request Number:', str(i+1), 'Ip:', str(proxy))
  
  try:
    response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=3)
    statusCode = webRequest(proxy)
    if (statusCode == 200):
      break
  except requests.exceptions.ConnectTimeout:
    print("Proxy Time out")
  except:
    print('Proxy Other Error')
  # finally:
  #   print('Proxy ', str(i+1), ': ', proxy)

print(len(proxies))
print(all_a_tag[0:3])

