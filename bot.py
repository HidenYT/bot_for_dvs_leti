from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep


delay = 0 # delay in seconds between clicking on buttons


lecture_link    = 'XXX' # example: https://vec.etu.ru/moodle/mod/lesson/view.php?id=12345
login           = 'XXX' # your moodle login
password        = 'XXX' # your moodle password

def gethtml(elem):
    return elem.get_attribute('outerHTML')

wd = webdriver.Chrome()

wd.get('https://vec.etu.ru/')
WebDriverWait(wd, timeout=10).until(
    lambda x: x.find_element(By.CSS_SELECTOR, 
                             '.btn.btn-primary.btn-block[value="Вход"]'
                            ))

login_element       = wd.find_element(By.CSS_SELECTOR, 'input#login_username')
password_element    = wd.find_element(By.CSS_SELECTOR, 'input#login_password')
login_button        = wd.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-block[value="Вход"]')
login_element.send_keys(login)
password_element.send_keys(password)
login_button.click()
sleep(delay)

wd.get(lecture_link)

lecture_title = wd.find_element(By.CSS_SELECTOR, 'div[role="main"] h2')

iid = lecture_link.split('id=')[1]

output_file = open(f'lectureId{iid}.html', 'w')
output_file.write('<html><body>')
output_file.write(gethtml(lecture_title))

while True:
    if 'остановились' in wd.page_source:
        wd.find_elements(By.CSS_SELECTOR, '.lessonbutton.standardbutton a.btn')[-1].click()
    if wd.find_elements(By.CSS_SELECTOR, 'button[type="submit"]'):
        page_h3 = wd.find_elements(By.CSS_SELECTOR, 'div[role="main"] h3')
        for h3 in page_h3:
            output_file.write(gethtml(h3))
        text = wd.find_elements(By.CSS_SELECTOR, 'div.box.contents p')
        for p in text:
            output_file.write(gethtml(p))
        next_button = wd.find_elements(By.CSS_SELECTOR,'button[type="submit"]')[-1]
        next_button.click()
        sleep(delay)
    elif wd.find_elements(By.CSS_SELECTOR, 'input#id_submitbutton'):
        chosen_options = set()
        while True:
            fields = wd.find_elements(By.CSS_SELECTOR, 'label.form-check-label')
            for field in fields:
                if field.text in chosen_options: continue
                check = field.find_element(By.TAG_NAME, 'input')
                chosen_options.add(field.text)
                check.click()
                send_button = wd.find_elements(By.CSS_SELECTOR, 'input#id_submitbutton')[0]
                send_button.click()
                sleep(delay)
                break
            if 'Это неправильный ответ' in wd.page_source: 
                wd.find_elements(By.CSS_SELECTOR, '.singlebutton button[type="submit"]')[0].click()
                sleep(delay)
                continue
            break
    else:
        break
output_file.write('</body></html>')
output_file.close()
wd.quit()