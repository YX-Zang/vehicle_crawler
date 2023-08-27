import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Crawler():
    def __init__(self, domain_url):
        self.driver = webdriver.Chrome()
        self.domain = domain_url

    def check_cookie_btn(self):
        wait = WebDriverWait(self.driver, 20)
        parent_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="usercentrics-root"]')))
        parent_el_shadow_root = parent_element.shadow_root
        time.sleep(5)
        accept_button = parent_el_shadow_root.find_element(
            By.CSS_SELECTOR,
            'button[data-testid="uc-accept-all-button"]'
        )
        print('click accept cookie button')
        accept_button.click()

    def action(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value='div[class="b-logo"] a[title="BMW"]').click()
        time.sleep(4)
        click_sequence = ['X1', 'F48', 'SAV', 'X1 18d', 'THA', 'Engine']
        for text in click_sequence:
            self.driver.find_element(
                by=By.CSS_SELECTOR,
                value=f'div span[title="{text}"]'
            ).click()
            time.sleep(2)


    def run(self):
        self.driver.get(self.domain)

        self.check_cookie_btn()

        # action
        self.action()




if __name__ == '__main__':
    target_url = 'https://www.partslink24.com'
    cr = Crawler(target_url)
    cr.run()

