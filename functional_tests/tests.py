from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about this awesome new online to-do app.
        # She goes to check it out
        self.browser.get(self.live_server_url)

        # She notices that the title and header mention To-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
                )

        # She types "Buy a peacock toy for my girl" in a text box
        inputbox.send_keys('Buy a peacock toy for my girl')

        # When she hits enter, the page updates and now the page lists
        # "1: Buy a peacock toy for my girl" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy a peacock toy for my girl')

        # There is still a text box inviting her to type more to-do items
        # She enters "Buy crayons"

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy crayons')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items in the to-do list
        self.wait_for_row_in_list_table('1: Buy a peacock toy for my girl')
        self.wait_for_row_in_list_table('2: Buy crayons')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy a peacock toy')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy a peacock toy')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user Hamid, comes along to the site,

        ## We use a new browsers session to ensure 
        ## that no information from Edith's browser is 
        ## coming through cookies or something

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Hamid visits the homepage. There is no sign
        # of Edith's list

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a peacock toy', page_text)
        self.assertNotIn('Buy crayons', page_text)

        # Hamid starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Take selfie with phone')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Take selfie with phone')

        # Hamid gets his own unique URL
        hamid_list_url = self.browser.current_url
        self.assertRegex(hamid_list_url, '/lists/.+')
        self.assertNotEqual(hamid_list_url, edith_list_url)

        # Again there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy a peacock toy', page_text)
        self.assertNotIn('Buy crayons', page_text)

        # Satisfied they both go to sleep


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
