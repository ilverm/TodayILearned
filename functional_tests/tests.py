import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate
from django.urls import reverse

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

activate('en')

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        options = webdriver.FirefoxOptions()
        #options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(10)
        self.browser.get(self.live_server_url)

        # create user
        self.browser.find_element(By.CLASS_NAME, 'signup-button').click()
        email_input = self.browser.find_element(By.NAME, 'email')
        email_input.send_keys('test@test.com')
        username_input = self.browser.find_element(By.NAME, 'username')
        username_input.send_keys('test@test.com')
        password1_input = self.browser.find_element(By.NAME, 'password1')
        password1_input.send_keys('testpassword')
        password2_input = self.browser.find_element(By.NAME, 'password2')
        password2_input.send_keys('testpassword')
        self.browser.find_element(By.XPATH, '//button[@value="create_account"]').click()

    def tearDown(self):
        self.browser.quit()

    def test_single_user_can_create_a_post(self):
        username_input = self.browser.find_element(By.NAME, 'username')
        username_input.send_keys('test@test.com')
        password_input = self.browser.find_element(By.NAME, 'password')
        password_input.send_keys('testpassword')
        self.browser.find_element(By.XPATH, '//input[@value="login"]').click()

        # Create post
        self.browser.find_element(By.CLASS_NAME, 'create-button').click()
        title_input = self.browser.find_element(By.NAME, 'title')
        title_input.send_keys('test title')
        slug_input = self.browser.find_element(By.NAME, 'slug')
        slug_input.send_keys('test-title')
        self.browser.execute_script("tinyMCE.activeEditor.selection.setContent('test content ')")
        source_input = self.browser.find_element(By.NAME, 'source')
        source_input.send_keys('http://www.test.com')
        tag_input = self.browser.find_element(By.NAME, 'tag')
        tag_input.send_keys('test_tag')
        self.browser.find_element(By.CLASS_NAME, 'create-btn').click()
        
        # Check if title in home page
        title_text = self.browser.find_element(By.CLASS_NAME, 'home-title').text
        self.assertEqual('test title', title_text)

        # Check if author is set correctly
        author_text = self.browser.find_element(By.CLASS_NAME, 'home-author').text
        self.assertEqual('test@test.com', author_text)

        # Check if the search bar works correctly
        search_text = self.browser.find_element(By.CLASS_NAME, 'search-bar')
        search_text.send_keys('test-tag')
        self.browser.find_element(By.CLASS_NAME, 'search-bar').click()
        title_text = self.browser.find_element(By.CLASS_NAME, 'home-title').text
        self.assertEqual('test title', title_text)

    def test_multiple_user_can_create_posts(self):
        # log first user in
        username_input = self.browser.find_element(By.NAME, 'username')
        username_input.send_keys('test@test.com')
        password_input = self.browser.find_element(By.NAME, 'password')
        password_input.send_keys('testpassword')
        self.browser.find_element(By.XPATH, '//input[@value="login"]').click()

        # create post --> first user is the author
        self.browser.find_element(By.CLASS_NAME, 'create-button').click()
        title_input = self.browser.find_element(By.NAME, 'title')
        title_input.send_keys('test title')
        slug_input = self.browser.find_element(By.NAME, 'slug')
        slug_input.send_keys('test-title')
        self.browser.execute_script("tinyMCE.activeEditor.selection.setContent('test content')")
        source_input = self.browser.find_element(By.NAME, 'source')
        source_input.send_keys('http://www.test.com')
        tag_input = self.browser.find_element(By.NAME, 'tag')
        tag_input.send_keys('test_tag')
        self.browser.find_element(By.CLASS_NAME, 'create-btn').click()

        # log first user out
        self.browser.find_element(By.CLASS_NAME, 'user-dropdown').click()
        self.browser.find_element(By.CLASS_NAME, 'logout-dropdown').click()

        # create second user
        self.browser.find_element(By.CLASS_NAME, 'signup-button').click()
        email_input = self.browser.find_element(By.NAME, 'email')
        email_input.send_keys('test2@test.com')
        username_input = self.browser.find_element(By.NAME, 'username')
        username_input.send_keys('test2@test.com')
        password1_input = self.browser.find_element(By.NAME, 'password1')
        password1_input.send_keys('testpassword2')
        password2_input = self.browser.find_element(By.NAME, 'password2')
        password2_input.send_keys('testpassword2')
        self.browser.find_element(By.XPATH, '//button[@value="create_account"]').click()

        # log second user in
        username_input = self.browser.find_element(By.NAME, 'username')
        username_input.send_keys('test2@test.com')
        password_input = self.browser.find_element(By.NAME, 'password')
        password_input.send_keys('testpassword2')
        self.browser.find_element(By.XPATH, '//input[@value="login"]').click()

        # create post --> second user is the author
        self.browser.find_element(By.CLASS_NAME, 'create-button').click()
        title_input = self.browser.find_element(By.NAME, 'title')
        title_input.send_keys('test title2')
        slug_input = self.browser.find_element(By.NAME, 'slug')
        slug_input.send_keys('test-title2')
        self.browser.execute_script("tinyMCE.activeEditor.selection.setContent('test content2')")
        source_input = self.browser.find_element(By.NAME, 'source')
        source_input.send_keys('http://www.test2.com')
        tag_input = self.browser.find_element(By.NAME, 'tag')
        tag_input.send_keys('test_tag2')
        self.browser.find_element(By.CLASS_NAME, 'create-btn').click()

        title_texts = self.browser.find_elements(By.CLASS_NAME, 'home-title')
        self.assertEqual('test title2', title_texts[0].text)
        self.assertEqual('test title', title_texts[1].text)

        author_texts = self.browser.find_elements(By.CLASS_NAME, 'home-author')
        self.assertIn('test2@test.com', author_texts[0].text)
        self.assertIn('test@test.com', author_texts[1].text)

    def test_italian_localization(self):
        # test english localization
        self.browser.get(self.live_server_url)
        en_signup_btn = self.browser.find_element(By.CLASS_NAME, 'signup-button').text
        self.assertEqual('Sign Up', en_signup_btn)

        # change language
        self.browser.find_element(By.CLASS_NAME, 'lang_btn').click()
        self.browser.find_element(By.CLASS_NAME, 'each_lang').click()

        # test italian localization
        it_signup_btn = self.browser.find_element(By.CLASS_NAME, 'signup-button').text
        self.assertEqual('Registrati', it_signup_btn)

        # test italian localization in search bar
        ita_search_bar = self.browser.find_element(By.CLASS_NAME, 'search-bar').get_attribute('placeholder')
        self.assertEqual('Cerca nel sito...', ita_search_bar)

        # change language
        self.browser.find_element(By.CLASS_NAME, 'lang_btn').click()
        self.browser.find_element(By.CLASS_NAME, 'each_lang').click()

        # test english localization in search bar
        en_search_bar = self.browser.find_element(By.CLASS_NAME, 'search-bar').get_attribute('placeholder')
        self.assertEqual('search the site...', en_search_bar)

    def test_personal_page(self):
        # log first user in
        username_input = self.browser.find_element(By.NAME, 'username')
        username_input.send_keys('test@test.com')
        password_input = self.browser.find_element(By.NAME, 'password')
        password_input.send_keys('testpassword')
        self.browser.find_element(By.XPATH, '//input[@value="login"]').click()

        # Create post
        self.browser.find_element(By.CLASS_NAME, 'create-button').click()
        title_input = self.browser.find_element(By.NAME, 'title')
        title_input.send_keys('test title')
        slug_input = self.browser.find_element(By.NAME, 'slug')
        slug_input.send_keys('test-title')
        self.browser.execute_script("tinyMCE.activeEditor.selection.setContent('test content ')")
        source_input = self.browser.find_element(By.NAME, 'source')
        source_input.send_keys('http://www.test.com')
        tag_input = self.browser.find_element(By.NAME, 'tag')
        tag_input.send_keys('test_tag')
        self.browser.find_element(By.CLASS_NAME, 'create-btn').click()

        # find and click user button
        self.browser.find_element(By.CLASS_NAME, 'user-dropdown').click()
        self.browser.find_element(By.CLASS_NAME, 'first-dropdown').click()
        # test title
        post_actions = self.browser.find_element(By.CLASS_NAME, 'singlepost-actions')
        self.assertTrue(post_actions)

        # log user out
        self.browser.find_element(By.CLASS_NAME, 'user-dropdown').click()
        self.browser.find_element(By.CLASS_NAME, 'logout-dropdown').click()

        # find and click author of test post
        self.browser.find_element(By.CLASS_NAME, 'home-author').click()
        test_title = self.browser.find_element(By.CLASS_NAME, 'home-title')
        self.assertTrue(test_title)
        
        try:
            post_actions = self.browser.find_element(By.CLASS_NAME, 'singlepost-actions')
        except NoSuchElementException:
            post_actions = None

        self.assertFalse(post_actions)
