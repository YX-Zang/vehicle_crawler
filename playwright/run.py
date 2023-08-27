from pprint import pprint
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class Playwrighr_tools():
    def __init__(self, playwright):
        self.base_setting(playwright)

    def behind_webdriver(self):
        behind_js = '''
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        '''
        self.page.add_init_script(behind_js)
    def base_setting(self, playwright):
        self.browser = playwright.chromium.launch(headless=False, slow_mo=100)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.behind_webdriver()

class Crawler(Playwrighr_tools):
    def __init__(self, domain_url, playwright):
        Playwrighr_tools.__init__(self, playwright)
        self.domain = domain_url

    layer_text = lambda self, selector: [i.text for i in BeautifulSoup(self.page.content(), 'lxml').select(selector)]

    def check_cookie_btn(self):
        self.page.click("text=Accept only essential services")

    def process_records(self, records):
        ls1 = []
        if isinstance(records, dict):
            records = [records]
        for item in records:
            if item.get('data', {}).get('records'):
                for data in item['data']['records']:
                    if data.get('link') and not data.get('id', '').startswith('_'):
                        ls1.append(data['link']['path'])
        return ls1

    def on_response(self, response):
        try:
            pprint(response.json())
        except Exception:
            pass

    def on_request(self, request):
        pprint('--------start---------')
        pprint(request.url)
        pprint(request.post_data)
        pprint('--------start---------')

    def test_action(self):
        # click BMW icon
        self.page.locator('div[class="b-logo"] a[title="BMW"]').click()
        self.page.wait_for_timeout(1000)
        click_sequence = ['X1', 'F48', 'SAV', 'X1 18d', 'THA', 'Engine']
        self.page.on('response', self.on_response)
        for text in click_sequence:
            self.page.click(f"text={text}")
            self.page.wait_for_timeout(500)

    def run(self):
        '''
        step 1: goto web page
        step 2: check cookie exist
        step 3: do action
        '''
        self.page.goto(self.domain, wait_until='networkidle')

        self.check_cookie_btn()

        # self.test_action()
        self.collect_link_action()
        print(self.queue_result.qsize())
        pprint('~')


if __name__ == '__main__':
    target_url = 'https://www.partslink24.com'
    with sync_playwright() as playwright:
        cr = Crawler(target_url, playwright)
        cr.run()