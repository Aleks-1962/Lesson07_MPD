""" Написать программу, которая собирает входящие письма из своего или тестового почтового ящика,
 и сложить информацию о письмах в базу данных (от кого, дата отправки, тема письма, текст письма)."""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions


def _parse_element(element, css_selector):
    result = WebDriverWait(element, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).text
    return result

def parse_email(element):
    item = {}

    item['from_name'] = _parse_element(
        element, 'span[class~="ns-view-message-head-sender-name"]')
    item['from_email'] = _parse_element(
        element, 'span[class~="mail-Message-Sender-Email"]')
    item['date'] = _parse_element(element,
                                  'div[class~="ns-view-message-head-date"]')
    item['subject'] = _parse_element(
        element, 'div[class~="mail-Message-Toolbar-Subject"]')
    item['text_messege'] = _parse_element(
        element, 'div.mail-Message-Body-Content')

    return item


driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')



title_site = 'Яндекс'

driver_get=driver.get('https://passport.yandex.ru/auth?origin=home_yandexid&retpath=https%3A%2F%2Fyandex.\
ru&backpath=https%3A%2F%2Fyandex.ru')



try:
    mail_button=driver.find_element_by_css_selector('span[class="Textinput Textinput_view_big-input Textinput_size_l"]')
    print( mail_button)

except exceptions.NoSuchElementException:
    print('LOGIN для авторизации почты не найден')

mail_button.click()

driver.title

if 'Авторизация' in driver.title:
    login_form = driver.find_element_by_css_selector('div[class="passp-auth"]')

    field_login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'passp-field-login')))
    field_login.send_keys('Bkmby.F')
    field_login.send_keys(Keys.ENTER)
    field_passwd = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'passp-field-passwd')))
    field_passwd.send_keys('Bkmby123')
    field_passwd.send_keys(Keys.ENTER)

field_mail_v = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'desk-notif-card__mail-title')))
field_passwd.send_keys(Keys.ENTER)


first_messege = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, 'ns-view-messages-item-wrap')
    )
)
first_messege.click()
collection =[]

while True:
    try:
        collection.insert_one(parse_email(driver))

        button_next = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'следущее')))
        button_next.click()
    except exceptions.TimeoutException:
        print('Сообщения закончились')
        break

driver.quit()