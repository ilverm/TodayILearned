import unittest
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

        # Sets up a logged-in user for testing.
        # We're creating and logging in a user to
        # facilitate testing scenarios where a logged-in
        # user is required, such as creating a post and
        # liking it. The logged-in user is made available
        # to all tests within the class.
        self.browser.get(self.live_server_url + reverse('create_account'))
        email_input = self.browser.find_element(By.NAME, 'email')
        email_input.send_keys('test@test.com')
        username_input = self.browser.find_element(By.NAME, 'username')
        username_input.send_keys('test@test.com')
        password1_input = self.browser.find_element(By.NAME, 'password1')
        password1_input.send_keys('testpassword')
        password2_input = self.browser.find_element(By.NAME, 'password2')
        password2_input.send_keys('testpassword')
        self.browser.find_element(By.XPATH, '//button[@value="create_account"]').click()

        username_input = self.browser.find_element(By.NAME, 'username')
        username_input.send_keys('test@test.com')
        password_input = self.browser.find_element(By.NAME, 'password')
        password_input.send_keys('testpassword')
        self.browser.find_element(By.XPATH, '//input[@value="login"]').click()

    def tearDown(self):
        self.browser.quit()

    def test_single_user_can_create_a_post(self):
        self.browser.get(self.live_server_url + reverse('create'))

        # Create article
        title_input = self.browser.find_element(By.NAME, 'title')
        title_input.send_keys('test title')
        slug_input = self.browser.find_element(By.NAME, 'slug')
        slug_input.send_keys('test-title')
        
        self.browser.execute_script("tinyMCE.activeEditor.selection.setContent('test content ')")

        source_input = self.browser.find_element(By.NAME, 'source')
        source_input.send_keys('http://www.test.com')
        tag_input = self.browser.find_element(By.NAME, 'tag')
        tag_input.send_keys('test_tag')
        self.browser.find_element(By.XPATH, '//input[@value="Submit"]').click()
        
        # Check if title in home page
        title_text = self.browser.find_element(By.CLASS_NAME, 'home-title').text
        self.assertIn('test title', title_text)

        # Check if author is set correctly
        author_text = self.browser.find_element(By.CLASS_NAME, 'tag_timesince').text
        self.assertIn('test@test.com', author_text)

        # Check if the search bar works correctly
        search_text = self.browser.find_element(By.CLASS_NAME, 'search-bar')
        search_text.send_keys('test-tag')
        self.browser.find_element(By.CLASS_NAME, 'search-bar').click()
        title_text = self.browser.find_element(By.CLASS_NAME, 'home-title').text
        self.assertIn('test title', title_text)

    def test_multiple_user_can_create_posts(self): ...