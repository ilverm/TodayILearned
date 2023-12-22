import unittest

from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError

from .forms import CustomUserCreationForm
from .models import CustomUser

class AuthenticationIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Create a test user for authentication testing
        self.user = CustomUser.objects.create_user(
            email='test@test.com',
            username='Testuser',
            password='test-insecure1'
        )

    def test_user_login(self):
        """
        Integration test for user login functionality.

        This test verifies that a user can successfully log in,
        and the session contains the expected information
        after the login.
        """
        login_successful = self.client.login(
            email='test@test.com',
            password='test-insecure1'
        )
        self.assertTrue(login_successful)

        # Check if user is logged in by checking the session
        self.assertTrue('_auth_user_id' in self.client.session)
        user_id_in_session = self.client.session['_auth_user_id']

        # Verify the user ID in the session matches the
        # expected user ID
        self.assertEqual(user_id_in_session, str(self.user.id))

class UserFormTest(TestCase):

    def test_empty_form(self):
        """
        Test CustomUser creation form to ensure that
        the 'email' and 'username' fields are present
        in the empty form.
        """
        form = CustomUserCreationForm()
        self.assertIn('email', form.fields)
        self.assertIn('username', form.fields)

    def test_form_is_valid(self):
        """
        Test CustomUser creation form to ensure that
        the constraints on username are working correctly.

        The constraints include:
        - Username is at least 8 characters long.
        - No spaces are present in the username.
        
        The constraints are implemented in the
        validate_username method in forms.py in the users
        app.
        """
        form_data = {
            'email': 'temp@temp.com',
            'username': 'temp-user',
            'password1': 'password-insecure1',
            'password2': 'password-insecure1',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid(self):
        """
        Test CustomUser creation form to ensure that
        the constraints on username are working correctly.

        The constraints include:
        - Username is at least 8 characters long.
        - No spaces are present in the username.

        The test case provides a username that is too short,
        violating the length constraint and checks whether
        the form correctly reports as invalid.
        
        The constraints are implemented in the
        validate_username method in forms.py in the users
        app.
        """
        form_data = {
            'email': 'temp@temp.com',
            'username': 'temp',
            'password': 'temp-insecure1'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

class UserModelTest(TestCase):

    def test_username_length_validation(self):
        """
        Test the username validator in the CustomUser model.

        The test case creates a CustomUser instance with a
        username that is less than 8 characters long, violating
        the length constraint. It then checks whether the
        validator correctly raises a ValidationError.

        The username validator is implemented in validators.py
        in the users app. It enforces the constraint that the
        username must be at least 8 characters long and must
        not contain spaces. 
        """
        temp_user = CustomUser.objects.create(
            email='temp@temp.com', 
            username='temp', 
            password='temp-insecure1'
        )
        self.assertRaises(ValidationError, temp_user.full_clean)

    def test_username_no_spaces_validation(self):
        """
        Test the username validator in the CustomUser model.

        The test case creates a CustomUser instance with a
        username that contains spaces, violating the constraint
        that the username must not have spaces. It then checks
        whether the validator correctly raises a ValidationError.

        The username validator is implemented in validators.py
        in the users app. It enforces the constraint that the
        username must be at least 8 characters long and must
        not contain spaces.
        """
        temp_user = CustomUser.objects.create(
            email='temp@temp.com',
            username=' temptemp',
            password='temp-insecure1'
        )
        self.assertRaises(ValidationError, temp_user.full_clean)

    def test_username_required(self):
        """
        Test the username blank validator in the CustomUser
        model.

        The test case creates a CustomUser instance with a
        missing username, violating the constraint that the
        username is required.

        The validator is expected to raise a ValidationError
        since the username field is set as "blank=False",
        indicating that it must not be left empty.
        """
        temp_user = CustomUser.objects.create(
            email='temp@temp.com',
            password='temp-insecure1'
        )
        self.assertRaises(ValidationError, temp_user.full_clean)

    def test_model_str_representation(self):
        """
        Test the __str__ method of the CustomUser model.

        The test case creates a CustomUser instance with a
        specified email. It then checks whether the __str__
        method correctly returns the email field.

        The __str__ method is expected to provide a
        human_readable representation of the user and, in this
        case, it should return the value of the 'email' field.
        """
        temp_user = CustomUser.objects.create(
            email='temp@temp.com',
            username='temptemp',
            password='temp-insecure1'
        )
        self.assertEqual(str(temp_user), 'temp@temp.com')