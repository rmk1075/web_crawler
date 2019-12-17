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

# hisnet = webdriver.Chrome('C:/Users/jjmin/Downloads/chromedriver', chrome_options=chrome_options)
hisnet = webdriver.Chrome('../chromedriver_win32_ver79/chromedriver', chrome_options=chrome_options)

# login page
hisnet.get(hisnet_login)

# login - id, password
hisnet.find_element_by_name('id').send_keys(LOGIN_INFO['id'])
hisnet.find_element_by_name('password').send_keys(LOGIN_INFO['password'])
# driver.find_element_by_name('id').send_keys(LOGIN_INFO['id'])
# driver.find_element_by_name('password').send_keys(LOGIN_INFO['password'])

# push login button
hisnet.find_element_by_xpath('//*[@id="loginBoxBg"]/table[2]/tbody/tr/td[5]/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input').click()

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
        semester = table.find_element_by_xpath('tbody/tr['+str(num)+']/td[1]').text
        semester = semester.split('-')[0] + semester.split('-')[1]

        hisnet.find_element_by_xpath('//*[@id="att_list"]/tbody/tr['+str(num)+']/td[6]/a').click()
        
        length = len(hisnet.find_element_by_id('div_'+semester).text.split('\n'))
        for i in range(3, length+1):
            temp_list = [semester]
            for j in range(6):
                # print(hisnet.find_element_by_xpath('//div[@id="div_'+semester+'"]/table/tbody/tr['+str(i)+']/td['+str(j+1)+']').text)
                temp_list.append(hisnet.find_element_by_xpath('//div[@id="div_'+semester+'"]/table/tbody/tr['+str(i)+']/td['+str(j+1)+']').text)
            grade_list.append(temp_list)

        num += 1
    except:
        break

# print(grade_list)
lecture_count = 0
general = 0.0
major = 0.0
else_list = []
for lecture in grade_list:
    #TODO: if grade F, ignore?
    #TODO: if senior, 공동체리더십훈련 - 0.5 point -> changed to 1????
    if '교양' in lecture[3] or '실무' in lecture[3]:
        lecture_count += 1
        general += float(lecture[4])
    elif '전공' in lecture[3]:
        major += float(lecture[4])
        lecture_count += 1
    else:
        else_list.append([lecture[2], lecture[3]])

    print(lecture)

print('총 이수 과목 수: ' + str(lecture_count))
print('총 이수 학점: ' + str(general + major))
print('교양 이수 학점: ' + str(general))
print('전공 이수 학점: ' + str(major))
