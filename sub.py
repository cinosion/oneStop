# import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# from selene import browser
from selene import config
from selene.browsers import BrowserName
# from selene.api import *
from webdriver_manager.chrome import ChromeDriverManager

#export ID,password to os environment
#you must delete this row on run
import idpass

#main class
class ScrapeLoginAuthSite():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.url = "https://www.ac04.tamacc.chuo-u.ac.jp/ActiveCampus/module/Login.php"
        #chrome driver -headless mode
        #options = Options()
        # options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        # options.headless = True
        #self.driver = webdriver.Chrome(options=options)
        #if you want debug
        #self.driver = webdriver.Chrome()

        config.browser_name = BrowserName.CHROME
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument('--headless')
        chrome_option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=chrome_option)

    def main(self):
        driver = self.driver
        #Login window
        print('login window open')
        driver.get(self.url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'button-submit')))
        username_box = driver.find_element_by_name('login')
        username_box.send_keys(self.username)
        password_box = driver.find_element_by_name('passwd')
        password_box.send_keys(self.password)
        submit_button = driver.find_element_by_class_name('button-submit')
        submit_button.submit()

        # Mypage window
        # if "https://www.ac04.tamacc.chuo-u.ac.jp/ActiveCampus/index_after.html" in driver.current_url:
            # module/MyPage.php
            # print("Mypage window open")
        print("don't know Mypage but window open")
        driver.get("https://www.ac04.tamacc.chuo-u.ac.jp/ActiveCampus/module/MyPage.php")
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
        html = driver.page_source
        with open('cplus.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("request succeed")
        return None

    # destractor
    def __del__(self):
        print("del:driver")
        self.driver.quit()

if __name__ == "__main__":
  login_id = idpass.identification
  login_pass = idpass.password
  text = ScrapeLoginAuthSite(login_id,login_pass).main()