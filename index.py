from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from time import sleep
import json, openpyxl

useragent = UserAgent()

options = webdriver.ChromeOptions()

options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0')
driver = webdriver.Chrome(executable_path=r'E:\Programms2\gathering\chromedriver.exe', options=options)

log_data = json.loads(open('data.json', 'r').read())
login = log_data['email']
password = log_data["password"]

PATH = r"E:\Programms2\gathering\data.xlsx"


def check(friend_l):
    driver.implicitly_wait(2)
    driver.find_element_by_class_name('zV_Nj').click()
    post_url = driver.current_url
    liked=[]
    for i in driver.find_elements_by_xpath('//a[@class="FPmhX notranslate MBL3Z"]'):
        liked.append(i.text)
    print()
    print(liked)
    print()
    for friend in friend_l.keys():
        if friend in liked:
            friend_l[friend][post_url] = "ok"
        else:
            if post_url not in friend_l[friend]:
                friend_l[friend][post_url] = 0
            else:
                friend_l[friend][post_url] += 1
    
def load():
    friends = {}
    excel = openpyxl.load_workbook(PATH)
    sheet = excel.active
    max_row = sheet.max_row
    for i in range(1, max_row+1):
        friends[sheet.cell(column = 1, row = i ).value] ={}
    for i in range(1, max_row+1):
        friends[ sheet.cell(column = 1, row = i ).value ].update( {sheet.cell(column = 2, row = i).value : sheet.cell(column = 3, row = i).value})
    return friends

def excelizing(friends):
    excel = openpyxl.load_workbook(PATH)
    sheet = excel.active
    i = 1
    for friend in friends.keys():
        for post in friends[friend].keys():
            sheet[f"A{i}"] = friend
            sheet[f"B{i}"] = post
            sheet[f"C{i}"] = friends[friend][post]
            i+=1
    excel.save(PATH)
    
def friend_check(friend_l, raw_l):
    for i in raw_l:
        if i.text in friend_l.keys():
            continue
        else:
            friend_l[i.text] = {}
    
friend_l = load()
print(friend_l)
try:
    driver.get('https://instagram.com')
    driver.implicitly_wait(5)
    inp_email, inp_pass = driver.find_elements_by_xpath('//*[@id="loginForm"]//*[@class="_2hvTZ pexuQ zyHYP"]')
    inp_email.send_keys(login)
    inp_pass.send_keys(password)
    inp_pass.send_keys(Keys.ENTER)
    driver.implicitly_wait(5)
    n = "'"
    driver.find_element_by_xpath(f'//img[@alt="red_command_of_nis{n}s profile picture"]').click()
    driver.find_element_by_link_text('Profile').click()
    driver.find_element_by_partial_link_text('followers').click()
    raw_l = driver.find_elements_by_xpath('//a[@class="FPmhX notranslate  _0imsa "]')
    friend_check(friend_l, raw_l)
    driver.find_element_by_xpath('//div[@class="eiUFA "]//button[@class="wpO6b  "]').click()
    print()
    print(friend_l)
    print()
    driver.implicitly_wait(3)
    posts = driver.find_elements_by_xpath('//div[@class="Nnq7C weEfm"]//a')
    for post in posts:
        driver.execute_script("arguments[0].click();", post)
        driver.implicitly_wait(2)
        check(friend_l)
    excelizing(friend_l)
finally:
    driver.close()
    driver.quit()