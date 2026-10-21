from django.test import TestCase
from django.urls import reverse


class RegistrationPageTests(TestCase):
    def test_registration_page_displays_form_fields(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)
        for field_name in (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
            'confirm_password',
        ):
            with self.subTest(field=field_name):
                self.assertContains(response, f'name="{field_name}"')
