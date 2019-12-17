#-*- coding:utf-8 -*-
## crawling source code - crawl the entire semester grade table from the hisnet haksa info by using selenium
## the user put in the hisnet account - id and password

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

hisnet_id = input('ID: ')
hisnet_pwd = input('Password: ')

LOGIN_INFO = {
    'id': hisnet_id,
    'password': hisnet_pwd
}

hisnet_login = 'https://hisnet.handong.edu/login/login.php'
hisnet_haksa_record = 'https://hisnet.handong.edu/haksa/record/HREC110M.php'

# chrome option object - headless setting
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

hisnet = webdriver.Chrome(
    'C:/Users/jjmin/Downloads/chromedriver', chrome_options=chrome_options)
# hisnet = webdriver.Chrome('C:/Users/jjmin/Downloads/chromedriver')

# login page
hisnet.get(hisnet_login)

# login - id, password
hisnet.find_element_by_name('id').send_keys(LOGIN_INFO['id'])
hisnet.find_element_by_name('password').send_keys(LOGIN_INFO['password'])
# driver.find_element_by_name('id').send_keys(LOGIN_INFO['id'])
# driver.find_element_by_name('password').send_keys(LOGIN_INFO['password'])

# push login button
hisnet.find_element_by_xpath(
    '//*[@id="loginBoxBg"]/table[2]/tbody/tr/td[5]/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input').click()

try:
    # enter to the hisnet haksa record page
    hisnet.get(hisnet_haksa_record)
except Exception:
    # when exception occurred - wrong account
    print('wrong id or pwd')
    exit()

grade_list = [['학기', '과목코드', '과목명', '이수구분', '학점', '성적', '평점']]

num = 2
table = hisnet.find_element_by_xpath('//*[@id="att_list"]')
while(True):
    try:
        semester = table.find_element_by_xpath(
            'tbody/tr['+str(num)+']/td[1]').text
        semester = semester.split('-')[0] + semester.split('-')[1]

        hisnet.find_element_by_xpath(
            '//*[@id="att_list"]/tbody/tr['+str(num)+']/td[6]/a').click()

        # length = hisnet.find_element_by_id('div_'+semester).text.split('\n')
        # for i in range(2, length):
        #     temp_list = [semester]
        #     for j in range(6):
        #         print(hisnet.find_element_by_xpath('//div[@id="div_'+semester+'"]/table/tbody/tr['+str(i)+']/td['+str(j+1)+']').text)
        #         temp_list.append(hisnet.find_element_by_xpath('//div[@id="div_'+semester+'"]/table/tbody/tr['+str(i)+']/td['+str(j+1)+']').text)
        #     grade_list.append(temp_list)

        print(hisnet.find_element_by_xpath(
            '//div[@id="div_'+semester+'"]/table/tbody/tr[3]/td[1]').text)

        # div = hisnet.find_element_by_id('div_'+semester)
        # div = hisnet.find_element_by_xpath('//div[@id="div_'+semester+'"]/table/tbody/tr[3]')

        # for i in range(2, len(div.text.split('\n'))):
        #     temp_list = [semester]
        #     for j in range(6):
        #         temp_list.append(div.find_element_by_xpath('/table/tbody/tr[3]/td['+str(j+1)+']').text)
        #         print(div.find_element_by_xpath('/table/tbody/tr[3]/td['+str(j+1)+']').text)
        #     grade_list.append(temp_list)

        # text = hisnet.find_element_by_id('div_'+semester).text.split('\n')

        # for i in range(2, len(text)):
        #     temp_list = [semester]
        #     for j in range(6):
        #         temp_list.append(text[i].split(' ')[j])
        #     grade_list.append(temp_list)

        num += 1
    except:
        break

print(grade_list)

# table = hisnet.find_element_by_xpath('//*[@id="att_list"]').text

# lines = []
# line = ''
# for word in table:
#     if word == '\n':
#         lines.append(line)
#         line = ''
#     else:
#         line += word

# year = []
# semester = []
# credit = []
# average = []
# for line in lines:
#     year.append(line.split(' ')[0])
#     semester.append(line.split(' ')[1])
#     credit.append(line.split(' ')[2])
#     average.append(line.split(' ')[3])
#
# print(year)
# print(semester)
# print(credit)
# print(average)

# tables = hisnet.find_elements_by_xpath('/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/div/table/tbody')
# for table in tables:
#     t = table.text
#     print(t)

# tables = []
# i = 1
# while(True):
#     try:
#         hisnet.find_element_by_xpath('//*[@id="att_list"]/tbody/tr['+str(i)+']/td[6]').click()
#         table = hisnet.findElements(By.xpath('//*[@id="att_list"]/tbody')).text
#         print(table)
#         # table = hisnet.find_element_by_xpath('//*[@id="att_list"]/tbody').text
#         # for j in range(1, len(table)):
#         #     /html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[3]/td/div[4]/table/tbody
#
#         i += 1
#     except:
#         break

# //*[@id="att_list"]/tbody/tr[3]
# print(tables)
