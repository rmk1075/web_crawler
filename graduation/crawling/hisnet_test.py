#-*- coding:utf-8 -*-
## test for db connection
## update new rows (the information of user from the hisnet)
## select the data

import sys
import datetime
import pymysql
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

def crawling(hisnet):
    #grade_list = [['학기', '과목코드', '과목명', '이수구분', '학점', '성적', '평점']]
    grade_list = []

    num = 2
    table = hisnet.find_element_by_xpath('//*[@id="att_list"]')
    while(True):
        try:
            semester = table.find_element_by_xpath(
                'tbody/tr['+str(num)+']/td[1]').text
            semester = semester.split('-')[0] + semester.split('-')[1]

            hisnet.find_element_by_xpath(
                '//*[@id="att_list"]/tbody/tr['+str(num)+']/td[6]/a').click()

            length = len(hisnet.find_element_by_id(
                'div_'+semester).text.split('\n'))
            for i in range(3, length+1):
                temp_list = [semester]
                for j in range(6):
                    temp_list.append(hisnet.find_element_by_xpath(
                        '//div[@id="div_'+semester+'"]/table/tbody/tr['+str(i)+']/td['+str(j+1)+']').text)
                grade_list.append(temp_list)

            num += 1
        except:
            break

    return grade_list

    # lecture_count = 0 # 총 이수 과목 수
    # general = 0.0 # 총 이수 교양 학점
    # major = 0.0 # 총 이수 전공 학점
    # else_list = [] # 기타 과목들
    # for lecture in grade_list:
    #     #TODO: if grade F, ignore?
    #     #TODO: if senior, 공동체리더십훈련 - 0.5 point -> changed to 1????
    #     if '교양' in lecture[3] or '실무' in lecture[3]:
    #         lecture_count += 1
    #         general += float(lecture[4])
    #     elif '전공' in lecture[3]:
    #         major += float(lecture[4])
    #         lecture_count += 1
    #     else:
    #         else_list.append([lecture[2], lecture[3]])

        # print(lecture)

    # print('총 이수 과목 수: ' + str(lecture_count))
    # print('총 이수 학점: ' + str(general + major))
    # print('교양 이수 학점: ' + str(general))
    # print('전공 이수 학점: ' + str(major))

def login(hisnet, LOGIN_INFO):
    # login - id, password
    hisnet.find_element_by_name('id').send_keys(LOGIN_INFO['id'])
    hisnet.find_element_by_name('password').send_keys(LOGIN_INFO['password'])

    # push login button
    hisnet.find_element_by_xpath(
        '//*[@id="loginBoxBg"]/table[2]/tbody/tr/td[5]/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input').click()

    try:
        # enter to the hisnet haksa record page
        hisnet.get(hisnet_haksa_record)
    except Exception:
        # when exception occurred - wrong account
        print('wrong id or pwd')
        sys.exit()

    return hisnet

if __name__ == "__main__":
    # input - id & pwd
    hisnet_id = input('ID: ').strip()
    hisnet_pwd = input('Password: ').strip()

    LOGIN_INFO = {
        'id': hisnet_id,
        'password': hisnet_pwd
    }

    hisnet_login = 'https://hisnet.handong.edu/login/login.php'
    hisnet_haksa_record = 'https://hisnet.handong.edu/haksa/record/HREC110M.php'

    # chrome option object - headless setting
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')

    # TODO: check the version of chromedriver
    try:
        hisnet = webdriver.Chrome('../chromedriver_win32_ver79/chromedriver', chrome_options=chrome_options)
    except:
        print('chromedriver version error')
        sys.exit()

    # login page
    hisnet.get(hisnet_login)

    # login
    hisnet = login(hisnet, LOGIN_INFO)

    # TODO: exception...?
    # check the last access
    conn = pymysql.connect(host='localhost', user='root', password='jjmin100705!', db='mydb', charset='utf8')
    curs = conn.cursor()

    query = 'select * from lastupdate where hisnetID=\''+LOGIN_INFO['id']+'\';'
    curs.execute(query)

    access = curs.fetchall()
    lecture_list = []
    # TODO: compare lastaccess with current date -> update the date
    if access == ():
        # crawling
        lecture_list = crawling(hisnet)

        # insert new lecture data to students
        try:
            for lecture in lecture_list:
                query = 'insert into students values (%s, %s, %s, %s, %s, %s, %s, %s);'
                val = (LOGIN_INFO['id'], lecture[0], lecture[1], lecture[2], lecture[3], float(lecture[4]), lecture[5], float(lecture[6]))
                curs.execute(query, val)
                conn.commit()

            # insert new data to lastupdate
            try:
                query = 'insert into lastupdate (hisnetID, lastAccess) values (\'' + LOGIN_INFO['id']+'\, NOW());'
                curs.execute(query)
                conn.commit()
            except:
                print('error during update the lastupdate')
        
        except:
            query = 'delete from students where id=\''+LOGIN_INFO['id']+'\';'
            curs.execute(query)
            conn.commit()
            print('error during update the lecture list')

    # TODO: update when the last update is over the 30 days ago
    elif datetime.timedelta(days=30) < datetime.datetime.today() - access[0][1]:
        print('has to be updated')
    else:
        # select from DB
        query = 'select * from students where id=\''+LOGIN_INFO['id']+'\';'
        curs.execute(query)
        lecture_list = curs.fetchall()

        print(lecture_list)

    conn.close()
