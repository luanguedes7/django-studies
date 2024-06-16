from django.test import TestCase
from authors.forms import RegisterForm

class AuthorRegisterFormUnitTest(TestCase):
    def test_first_name_placeholder_is_correct(self):
        form = RegisterForm()