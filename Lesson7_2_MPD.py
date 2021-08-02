from selenium import webdriver
from selenium.common import exceptions


collection =[]

driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')


#url = 'https://www.mvideo.ru'
title_site = 'М.Видео'

driver.get('https://www.mvideo.ru')

assert title_site in driver.title


try:
    best_sellers = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[4]/div/div[1]/div/h2[1]')
    print(best_sellers)
except exceptions.NoSuchElementException:
    print('Best_sellers не найден!!!')


goods = best_sellers.find_elements_by_css_selector('li.gallery-list-item')

print (goods)
goods = [i.get_attribute('span') for i in goods]
print (goods)

item = {}
for it in goods:
    item['title'] = it.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('innerHTML')


    item['good_link'] = it.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('href')

    item['price'] = float(
        it.find_element_by_css_selector('div.c-pdp-price__current').get_attribute('innerHTML')\
            .replace('&nbsp;', '').replace('¤', ''))

    item['image_link'] = it.find_element_by_css_selector('img[class="lazy product-tile-picture__image"]')\
        .get_attribute('src')

    print(collection.update_one({'good_link': item['good_link']}, {'$set': item},upsert=True))

driver.quit()
