#-*- coding:utf-8 -*-
## crawling source code - crawl the entire semester grade table from the hisnet haksa info by using selenium
## the user put in the hisnet account - id and password

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

def login_check(hisnet_id, hisnet_pwd):
    # hisnet_id = input('ID: ')
    # hisnet_pwd = input('Password: ')

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
    hisnet = webdriver.Chrome('chromedriver/chromedriver', chrome_options=chrome_options)


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
        return True
    except Exception:
        # when exception occurred - wrong account
        print('wrong id or pwd')
        return False
