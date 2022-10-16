from django.test import TestCase

from main.models import Customer

class WebsiteTests(TestCase):
    def test_page_is_created_successfully(self):
        customer = Customer(
            first_name='yanuar',
            last_name='home'
        )
        customer.save()