from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from glob import glob
from os.path import exists
from os import makedirs

word_links_files = glob('./links/*_links.txt')

user_phone_number = input('enter phone number: ')

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

sleep(4)

counter = 0

for single_word_link in word_links_files:

    file_name = single_word_link.split('\\')

    file_content = open(single_word_link,'r',encoding='utf-8').readlines()

    for single_url in file_content:
        counter += 1

        is_exist = False
        is_word_title_exist = False

        if exists('./data/'+str(file_name[1])):

            for line in open('./data/'+str(file_name[1]),'r',encoding='utf-8').readlines():
                if line.find(single_url) > -1:
                    is_exist = True
                    break

        if is_exist == True:
            print(str(counter) +' exist')
            continue
        
        try:
            driver.get(single_url)
            sleep(2)
        except:
            continue

        current_word_data = {'title':None,'desc':list(),'examples':list(),'english':list(),'estelah_ha':list(),'ham_neshin':list()}

        try:
            word_title = driver.find_element(By.CSS_SELECTOR,'#WordPosDiv > div.p-en-bold')
            is_word_title_exist = True
        except:
            pass

        try:
            word_title = driver.find_element(By.CSS_SELECTOR,'#WordPosDiv > div.p-fa-bold')
            is_word_title_exist = True
        except:
            pass

        if not is_word_title_exist:
            continue

        current_word_data['title'] = word_title.text
        word_desc = driver.find_elements(By.CSS_SELECTOR,'#atlas_menu_desc > div > p')

        for single_word_desc in word_desc:
            current_word_data['desc'].append(single_word_desc.text)

        tab_buttons = driver.find_elements(By.CSS_SELECTOR,'span.atlas-menu')

        for single_tab_button in tab_buttons:
            if single_tab_button.text.find('مثال') > -1:
                single_tab_button.click()

                sleep(1)

                try:
                    more_example_button = driver.find_element(By.CSS_SELECTOR,'#div_title')
                    more_example_button.click()

                    sleep(1)

                except:
                    pass

                examples = driver.find_elements(By.CSS_SELECTOR,'#atlas_menu_desc > div > p')

                for single_example in examples:
                    current_word_data['examples'].append(single_example.text)

                continue

            elif single_tab_button.text.find('English') > -1:
            
                single_tab_button.click()

                sleep(1)

                english_text = driver.find_elements(By.CSS_SELECTOR,'#atlas_menu_desc > div')

                for single_english_text in english_text:
                    current_word_data['english'].append(single_english_text.text)

                continue

            elif single_tab_button.text.find('همنشین') > -1:

                single_tab_button.click()

                sleep(1)

                hamneshins = driver.find_elements(By.CSS_SELECTOR,'#atlas_menu_desc > div')

                for single_hamneshin in hamneshins:
                    current_word_data['ham_neshin'].append(single_hamneshin.text)

                continue

            elif single_tab_button.text.find('اصطلاح') > -1:
                single_tab_button.click()

                sleep(1)

                estelah_ha = driver.find_elements(By.CSS_SELECTOR,'#atlas_menu_desc > div')

                for single_estelah in estelah_ha:
                    current_word_data['estelah_ha'].append(single_estelah.text)

                continue

        if not exists('./data/'):
            makedirs('data')

        with open('./data/'+str(file_name[1]),'a',encoding='utf-8') as atlas_ir_txt_file:
            atlas_ir_txt_file.write('word: ' + current_word_data['title'] + '\n')

            atlas_ir_txt_file.write('desc: \n')

            for single_word_desc in current_word_data['desc']:
                atlas_ir_txt_file.write(single_word_desc + '\n')

            atlas_ir_txt_file.write('examples: \n')

            for single_word_example in current_word_data['examples']:
                atlas_ir_txt_file.write(single_word_example + '\n')

            atlas_ir_txt_file.write('english: \n')

            for single_word_english in current_word_data['english']:
                atlas_ir_txt_file.write(single_word_english + '\n')

            atlas_ir_txt_file.write('همنشین: \n')

            for single_word_hamneshin in current_word_data['ham_neshin']:
                atlas_ir_txt_file.write(single_word_hamneshin + '\n')

            for single_word_estelah in current_word_data['estelah_ha']:
                atlas_ir_txt_file.write(single_word_estelah + '\n')

            atlas_ir_txt_file.write('url: ' + driver.current_url + '\n')

            atlas_ir_txt_file.write('='*150 + '\n')

        print(str(counter) + ' ' + current_word_data)
        print('='*150)


print('success')