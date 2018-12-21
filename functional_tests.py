from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about this awesome new online to-do app.
        # She goes to check it out
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn('1: Buy a peacock toy for my girl', [row.text for row in rows])

        # There is still a text box inviting her to type more to-do items
        # She enters "Buy crayons"

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy crayons')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items in the to-do list

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn('1: Buy a peacock toy for my girl', [row.text for row in rows])
        self.assertIn('2: Buy crayons', [row.text for row in rows])
        # Edith wonder if the website will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail('finish the test!')

        # She visits that URL - her to-do list is there.

        # Satisfied she goes back to sleep.

if __name__ == '__main__':
    unittest.main()
