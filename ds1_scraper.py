from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import csv
import time

url = 'https://opensea.io/assets/matic/0x2953399124f0cbb46d2cbacd8a89cf0599974963/101324149589609765444097150160926508741381014360825123442161062676180034912326'

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)
nft_links = ['https://opensea.io/assets/0x37a03d4af1d7046d1126987b20117a0fdcbf6535/684', 'https://opensea.io/assets/0x10064373e248bc7253653ca05df73cf226202956/5455',
            'https://opensea.io/assets/0xafef885027a59603dff7837c280dad772c476b82/2698', 'https://opensea.io/assets/0x63f4392f994a5fb1730b8f4d1c42d99581623013/141',
            'https://opensea.io/assets/matic/0x2953399124f0cbb46d2cbacd8a89cf0599974963/101324149589609765444097150160926508741381014360825123442161062479367453540429',
            'https://opensea.io/assets/0x10064373e248bc7253653ca05df73cf226202956/7822', 'https://opensea.io/assets/0x10064373e248bc7253653ca05df73cf226202956/8812',
            'https://opensea.io/assets/0xcbc67ea382f8a006d46eeeb7255876beb7d7f14d/6748', 'https://opensea.io/assets/matic/0x2953399124f0cbb46d2cbacd8a89cf0599974963/101324149589609765444097150160926508741381014360825123442161062568427895390283',
            'https://opensea.io/assets/0x8143512918e962bd6c74c6db1235215e3f72ba43/38600030007',
            ]

dataset1 = []
for i in nft_links:
    driver.get(i)
    try:
        collection_name =  driver.find_element(By.CLASS_NAME, "CollectionLink--link").text
    except NoSuchElementException:
        collection_name = 'Not Found'
    #alt = get parent div with class item--collection-detail
    try:
        name = driver.find_element(By.CLASS_NAME, "item--title").text
    except NoSuchElementException:
        name = 'Not Found'
    ownersection = driver.find_element(By.CLASS_NAME, 'item--counts')
    try:
        number_of_owners = driver.find_element(By.CSS_SELECTOR, '#main > div > div > div > div.fresnel-container.fresnel-greaterThanOrEqual-lg > div > div.item--wrapper > div.item--main > section.item--counts > button:nth-child(1)').text.split('\n')[1][0:2]
    except NoSuchElementException:
        number_of_owners = "Not Found/Single Owner"
    try:
        favourites = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[1]/article/header/div[2]/p/div').text
    except NoSuchElementException:
        favourites = "Not Found"
    #alt //*[@id="main"]/div/div/div/div[2]/div/section[2]/button[2]
    #alt = get .text value of //*[@id="main"]/div/div/div/div[2]/div/article/header/div[2]/p/div xpath (top fav icon)
    #driver.find_element(By.XPATH, '//*[@id="Header react-aria-1"]/i[2]').click()
    try:
        avg_price = driver.find_element(By.CLASS_NAME, "PriceHistoryStats--value").text.split('Ξ')[1]
    except NoSuchElementException:
        avg_price = "No item activity yet"
    try:
        price_history = ""
    except NoSuchElementException:
        price_history = "Not Found"
    try:
        image = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[1]/article/div/div/div/div/div/div/img')
        image_url = image.get_attribute('src')
    except NoSuchElementException:
        image_url = "Not Found"
    try:
        audio = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[1]/article/div/div/div/div/div/audio')
        audio_url = audio.get_attribute('src')
    except NoSuchElementException:
        audio_url = "Not Found"
    try:
        description_section = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[1]/section/div/div[1]')
        description = description_section.find_element(By.CLASS_NAME, 'item--description-text').text
    except NoSuchElementException:
        description = "Not Found"
    properties_final = []
    try:
        properties_section =  driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[1]/section/div/div[2]')
        try:
            props = properties_section.find_element(By.CLASS_NAME, 'item--properties')
            properties = props.find_elements(By.TAG_NAME, 'a')
            for property in properties:
                prop_type = property.find_element(By.CLASS_NAME, 'Property--type').text
                prop_value = property.find_element(By.CLASS_NAME, 'Property--value').text
                properties_final.append(f"{prop_type}: {prop_value}")
        except StaleElementReferenceException:
            properties_section.click()
            properties = properties_section.find_elements(By.TAG_NAME, 'a')
            for property in properties:
                prop_type = property.find_element(By.CLASS_NAME, 'Property--type').text
                prop_value = property.find_element(By.CLASS_NAME, 'Property--value').text
                properties_final.append(f"{prop_type}: {prop_value}")
    except NoSuchElementException:
        properties_final =  "No Properties"
    try:
        about_span = driver.find_element(By.XPATH, '//span[starts-with(., "About")]') 
        span_parent = about_span.find_element(By.XPATH, './/parent::button//parent::div//parent::div')
        span_parent.click()
        about_collection = span_parent.find_element(By.CLASS_NAME, 'item--about-container').text
    except NoSuchElementException:
        about_collection =  "Not Found"

    #details
    time.sleep(2)
    details = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[1]/section/div/div[last()]')
    details.click()
    #contract_address_url = driver.find_element(By.XPATH, '//*[@id="Body react-aria-6"]/div/div/div/div[1]/span/a').get_attribute('href')
    contract_address = i.split('/')[-2]
    token_id = int(i.split('/')[-1])
    info_section = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[1]/section/div')
    token_standard = driver.find_elements(By.CLASS_NAME, 'jmAsQO')[2].text
    block_chain = driver.find_elements(By.CLASS_NAME, 'jmAsQO')[3].text

    try:
        owner = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[2]/section[2]/div/div/a').text
    except NoSuchElementException:
        try:
            driver.execute_script("window.scrollTo(0, 0)") 
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[2]/section[2]/button[1]').click()
            try:
                owners_popup = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div')
                print("DIV 11 Code")
                owners_lists_section = owners_popup.find_element(By.TAG_NAME, 'section')
                time.sleep(5)
                owners_lists = owners_lists_section.find_element(By.TAG_NAME, 'ul')
                owners = owners_lists.find_elements(By.TAG_NAME, 'li')
                owner = owners[0].text.split()[0]
            except NoSuchElementException:
                owners_popup = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div')
                print("DIV 7 Code")
                time.sleep(5)
                owners_lists = owners_popup.find_element(By.TAG_NAME, 'ul')
                owners = owners_lists.find_elements(By.TAG_NAME, 'li')
                owner = owners[0].text.split()[0]
        except NoSuchElementException:
            owner = "Unable to find owner info"
    element = driver.find_element(By.XPATH, "//body")
    element.send_keys(Keys.ESCAPE)
    try:
        owner_id = owner
    except NoSuchElementException:
        owner_id = owner

    dataset1.append([collection_name, name, owner, owner_id , number_of_owners, favourites, 
                    avg_price, price_history, image_url, audio_url, description, 
                    properties_final, about_collection, contract_address, token_id, 
                    token_standard, block_chain ])

with open('nft.csv', 'w', newline='', encoding="utf-8") as file: 
    writer = csv.writer(file)
    headers = ['collection_name', 'nft_name', 'owner_name', 'owner_id', 'number_of_owners',
                'total_favourites', 'avg_price', 'price_history', 'image', 'audio', 'description',
                'properties', 'about_collection', 'contract_address', 'token_id', 'token_standard',
                'block_chain' ]
    writer.writerow(headers)
    for data in dataset1:
        writer.writerow(data)