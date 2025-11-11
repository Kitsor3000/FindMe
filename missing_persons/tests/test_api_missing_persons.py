from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from missing_persons.models import MissingPerson
import datetime

class MissingPersonsAPITest(TestCase):
    def setUp(self):
        # Створюємо користувача
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Створюємо тестові записи
        MissingPerson.objects.create(
            user=self.user,
            full_name='Іван Петренко',
            status='missing',
            city='Київ',
            region='Київська',
            description='Зник у парку',
            missing_date=datetime.date(2024, 5, 10)
        )
        MissingPerson.objects.create(
            user=self.user,
            full_name='Олег Коваль',
            status='found',
            city='Львів',
            region='Львівська',
            description='Знайдений у місті',
            missing_date=datetime.date(2024, 6, 1)
        )

    def test_get_missing_persons_list(self):
        """Перевірка, що API повертає правильну кількість записів"""
        url = reverse('api_missing_persons_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('persons', response.json())
        self.assertEqual(len(response.json()['persons']), 2)
        self.assertEqual(response.json()['persons'][0]['full_name'], 'Іван Петренко')
