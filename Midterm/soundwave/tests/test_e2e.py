from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class OrderEndToEndTests(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_user_can_place_order(self):
        self.browser.get(self.live_server_url + '/')
        self.browser.find_element_by_name('product').send_keys('Product Name')
        self.browser.find_element_by_name('quantity').send_keys('2')
        self.browser.find_element_by_name('submit').click()
        self.assertIn('Order placed successfully', self.browser.page_source)

