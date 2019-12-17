#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

LOGIN_INFO = {
    'id': 'rmk1075',
    'password': 'jjmin100705'
}

hisnet_login = 'https://hisnet.handong.edu/login/login.php'
hisnet_haksa_record = 'https://hisnet.handong.edu/haksa/record/HREC110M.php'

# chrome option object - headless setting
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

hisnet = webdriver.Chrome('C:/Users/jjmin/Downloads/chromedriver', chrome_options = chrome_options)
# hisnet = webdriver.Chrome('C:/Users/jjmin/Downloads/chromedriver')

# login page
hisnet.get(hisnet_login)

# login - id, password
hisnet.find_element_by_name('id').send_keys(LOGIN_INFO['id'])
hisnet.find_element_by_name('password').send_keys(LOGIN_INFO['password'])
# driver.find_element_by_name('id').send_keys(LOGIN_INFO['id'])
# driver.find_element_by_name('password').send_keys(LOGIN_INFO['password'])

# push login button
hisnet.find_element_by_xpath('//*[@id="loginBoxBg"]/table[2]/tbody/tr/td[5]/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input').click()

# enter to the hisnet haksa record page 
hisnet.get(hisnet_haksa_record)

table = hisnet.find_element_by_xpath('//*[@id="att_list"]').text
# print(table)

lines = []
line = ''
for word in table:
    if word == '\n':
        lines.append(line)
        line = ''
    else:
        line += word

year = []
semester = []
credit = []
average = []
for line in lines:
    year.append(line.split(' ')[0])
    semester.append(line.split(' ')[1])
    credit.append(line.split(' ')[2])
    average.append(line.split(' ')[3])

print(year)
print(semester)
print(credit)
print(average)

# with requests.Session() as s:
#     # login
#     login_req = s.post(hisnet_login, data=LOGIN_INFO)

#     if login_req.status_code != 200:
#         raise Exception('login fail. check the id and pwd')
#     else:
#         print(login_req.status_code)

#     # access to the haksa record info page
#     haksa_record_page = s.get(hitnet_haksa_record).text
#     print(haksa_record_page)
