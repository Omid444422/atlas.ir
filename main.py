from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from os.path import exists
from os import makedirs

user_phone_number = input('enter phone number: ')

word_links_url_exist = None

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

driver.get('http://www.atlas.ir/Login/?u=')

sleep(5)

phone_number_input = driver.find_element(By.CSS_SELECTOR,'#PhoneText')
phone_number_input.send_keys(user_phone_number)

sleep(1)

login_button = driver.find_element(By.CSS_SELECTOR,'#PhoneBtn')
login_button.click()

sleep(30)

login_button_with_code = driver.find_element(By.CSS_SELECTOR,'#PhoneBtn')
login_button_with_code.click()

sleep(7)

word_containers_elements = driver.find_elements(By.CSS_SELECTOR,'.link-box-small-a')
word_containers_url = list()

for single_word_container_element in word_containers_elements:
        word_containers_url.append(single_word_container_element.get_attribute('href'))

word_links = list()

for single_word_container_url in word_containers_url:
    driver.get(single_word_container_url)

    sleep(5)

    word_container_name = driver.find_element(By.CSS_SELECTOR,'#LogoId > a > span').text

    is_ended = False
    counter = 1

    if exists('./links/' + str(word_container_name)+'_links.txt'):
        file = open('./links/'+word_container_name+'_links.txt','r',encoding='utf-8').readlines()
        last_recieved_word_link = file[-1].split('?')[1].split('&')[0].split('=')[1]
        counter = int(last_recieved_word_link) 

    while True:

        driver.get(single_word_container_url + '&l='+str(counter))

        sleep(3)
        
        word_links_elements = driver.find_elements(By.CSS_SELECTOR,'a.noformat2')

        if len(word_links_elements) == 0:
            is_ended = True
            break

        for index,single_word_element in enumerate(word_links_elements):

            if index <=1: continue
            try:
                
                if single_word_element.get_attribute('href').find('word') > -1:

                    word_links.append(single_word_element.get_attribute('href'))
                    print(single_word_element.get_attribute('href'))
                    print('='*150)
                    continue

            except:
                pass
            
        if is_ended:
            break
        
        if not exists('./links'):
            makedirs('links')

        for single_word_link in word_links:
            with open('./links/'+word_container_name+'_links.txt','a',encoding='utf-8') as word_links_url_txt:
                word_links_url_txt.write(single_word_link + '\n')
        
        counter += 15
        word_links = list()

print('*'*200)
print('success')
