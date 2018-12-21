from selenium import webdriver
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

        # She notices that the title mentions To-do lists.
        self.assertIn('To-Do', self.browser.title)
        self.fail('finish the test!')

        # She is invited to enter a to-do item right away

        # She types "Buy a peacock toy for my girl" in a text box

        # When she hits enter, the page updates and now the page lists
        # "1: Buy a peacock toy for my girl" as an item in a to-do list

        # There is still a text box inviting her to type more to-do items
        # She enters "Buy crayons"

        # The page updates again, and now shows both items in the to-do list

        # Edith wonder if the website will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is there.

        # Satisfied she goes back to sleep.

if __name__ == '__main__':
    unittest.main()
