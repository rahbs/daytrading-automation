from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

# kr.investing.com 접속
baseUrl = 'https://kr.investing.com'
driver = webdriver.Chrome()
driver.get(baseUrl+'/equities/south-korea')
driver.maximize_window()

#로그인
email = 'rahbs@naver.com'
password = '########'
driver.find_element_by_xpath('/html/body/div[5]/header/div[1]/div/div[4]/span[1]/div/a[1]').click()
driver.find_element_by_xpath('//*[@id="loginFormUser_email"]').send_keys(email)
driver.find_element_by_xpath('//*[@id="loginForm_password"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="signup"]/a').click()
time.sleep(1)

# '코스피 200' 클릭
option = driver.find_element_by_xpath('//*[@id=37427]')
option.click()
time.sleep(1)

# # 코스피 200 종목 리스트
html = driver.page_source
soup = BeautifulSoup(html,features='lxml')
KOSPI200_elems = soup.select('td.bold.left.noWrap.elp.plusIconTd > a')
# KOSPI200_elems = driver.find_elements_by_css_selector('td.bold.left.noWrap.elp.plusIconTd')

KOSPI200_names = []
KOSPI200_links = []
for elem in KOSPI200_elems:
    # print(elem.select_one('a'))
    # print(elem.get('title'))
    KOSPI200_names.append(elem.get('title'))
    KOSPI200_links.append(elem.get('href'))
print('length: ', len(KOSPI200_elems))

for i in range(67,68):
    print(i)
    links = KOSPI200_links[i*3:]
    print(links)
    for cnt, link in enumerate(links):
        # 해당 족목의 '과거 데이터' url로 들어가기 
        url = baseUrl + link + '-historical-data'
        driver.get(url)
        html = driver.page_source
        time.sleep(1)

        # 해당 종목의 종목 코드 출력
        html = driver.page_source
        soup = BeautifulSoup(html, features='lxml')
        stock_code = soup.select_one('#leftColumn > div.instrumentHead > h1')
        print(stock_code)

        # 날짜 선택 클릭
        action = ActionChains(driver)
        driver.find_element_by_xpath("//*[@id='widgetFieldDateRange']").click()
        time.sleep(1)

        # start_date 입력 (end_date: 현재 날짜)
        driver.find_element_by_xpath("//*[@id='startDate']").clear()
        start_date = driver.find_element_by_xpath("//*[@id='startDate']").send_keys('2010/01/01')
        time.sleep(1)

        # '신청합니다' 클릭
        driver.find_element_by_xpath('//*[@id="applyBtn"]').click()
        time.sleep(2)

        # '다운로드' 클릭
        driver.find_element_by_xpath('//*[@id="column-content"]/div[4]/div/a').click()
        print(i*3+cnt, ': ', links[cnt], ' downloaded')
        #break
    
    # 웹브라우저 닫기
    driver.close()

# 웹브라우저 닫기
#driver.close()
