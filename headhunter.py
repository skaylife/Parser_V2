# https://hh.ru/search/vacancy?items_on_page=100&text=python
# https://hh.ru/search/vacancy?items_on_page=1&text=python&area=1002
# &area=1002 / Минск

import requests
from bs4 import BeautifulSoup

# # Кол-во вакансий на одной странице
items = 100
# # Запрос для поиска
qeury = 'python'
# # Сам url
url = f'https://hh.ru/search/vacancy?items_on_page={items}&text={qeury}'


# Заголовок для сайта
headers = {
  'Host': 'hh.ru',
  'User-Agent': 'Safari',
  'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

# headers = {
#   'Host': 'hh.ru',
#   'User-Agent': 'Safari',
#   'Accept': '*/*',
#   'Accept-Encoding': 'gzip, deflate, br',
#   'Connection': 'keep-alive'
# }



def extract_max_page():


  # Создаем запрос с заголовком для сайта
  hh_requests = requests.get(url, headers=headers)

  # Создаем объект супа 
  hh_soup = BeautifulSoup(hh_requests.text, 'html.parser')


  # Вытаскиваем заначения для получения кол-во стр.
  paginator = hh_soup.find_all("span", {'class': 'pager-item-not-in-short-range'})


  pages = []



  # pages = paginator.find_all('a')

  # Проходимся циклом чтоб вытащить число страниц с запросом
  for page in paginator:
    pages.append(int(page.find('a').text))


  return  pages[-1] # Берём последний запрос

# Цикл от 0 до кол-во max-page
# for page in range(max_page):
#   print(f'page={page}')


# Функция конкретно вытаскивающая карточку
def extract_job(html):
  title = html.find('a').text
  company = html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text
  company = company.strip()#
  city = (html.find('span', {'class': 'vacancy-serp-item__meta-info'})).text
  return {'title': title, 'company': company, 'city': city}

# Функция по пербору карточек hh
def extract_hh_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f'Парсинг страницы {page}')
    result = requests.get(f'{url}&page={page}', headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class': 'vacancy-serp-item'})
    # Вытаскиваем текст ссылки 
    for result in results:
      job = extract_job(result)
      jobs.append(job)



  return jobs

# Вызов всех функция для парсинга
def get_jobs():
  max_page =  extract_max_page()
  jobs = extract_hh_jobs(max_page)
  return jobs

