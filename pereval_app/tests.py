from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Coords, Pereval, Image


class PerevalAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'fam': 'Иванов',
            'name': 'Иван',
            'otc': 'Иванович',
            'phone': '+79991234567'
        }
        self.user = User.objects.create(**self.user_data)

        self.coords_data = {
            'latitude': '45.3842',
            'longitude': '7.1525',
            'height': '1200'
        }
        self.coords = Coords.objects.create(**self.coords_data)

        self.pereval_data = {
            'title': 'Тестовый перевал',
            'beauty_title': 'Тест',
            'other_titles': 'Тест',
            'connect': 'Тест',
            'user': self.user,
            'coords': self.coords,
            'status': 'new'
        }
        self.pereval = Pereval.objects.create(**self.pereval_data)

        self.image_data = {
            'pereval': self.pereval,
            'data': None,
            'title': 'Тестовое изображение'
        }
        self.image = Image.objects.create(**self.image_data)

    def test_create_pereval(self):
        url = reverse('submit-data')
        data = {
            "title": "Новый перевал",
            "beauty_title": "Новый",
            "other_titles": "Новый перевал",
            "connect": "Соединяет долины",
            "user": self.user_data,
            "coords": self.coords_data,
            "level": {
                "winter": "1A",
                "summer": "1B",
                "autumn": "",
                "spring": ""
            },
            "images": [
                {
                    "data": None,
                    "title": "Вид с севера"
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Запись успешно создана')
        self.assertTrue(response.data['id'] > 0)

    def test_get_pereval_list(self):
        url = reverse('submit-data') + '?user__email=' + self.user.email
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.pereval.title)

    def test_get_pereval_detail(self):
        url = reverse('submit-data-detail', kwargs={'pk': self.pereval.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.pereval.title)

    def test_update_pereval(self):
        url = reverse('submit-data-detail', kwargs={'pk': self.pereval.id})
        data = {
            "title": "Обновленный перевал",
            'beauty_title': 'нов. пер.',
            'other_titles': 'Обновлённое доп. наименование',
            'connect': 'Тест',
            "coords": {
                "latitude": "46.3842",
                "longitude": "8.1525",
                "height": "1300"
            },
            "level": {
                "winter": "2A",
                "summer": "1B",
                "autumn": "",
                "spring": ""
            }
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Запись успешно обновлена')

        # Проверяем обновленные данные
        updated_pereval = Pereval.objects.get(id=self.pereval.id)
        self.assertEqual(updated_pereval.title, "Обновленный перевал")
        self.assertEqual(str(updated_pereval.coords.latitude), "46.3842")

    def test_update_user_data_fails(self):
        url = reverse('submit-data-detail', kwargs={'pk': self.pereval.id})
        data = {
            "user": {
                "email": "new@example.com",
                "fam": "Петров"
            }
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Редактирование поля', response.data['message'])

    def test_update_non_new_status_fails(self):
        # Меняем статус перевала
        self.pereval.status = 'accepted'
        self.pereval.save()

        url = reverse('submit-data-detail', kwargs={'pk': self.pereval.id})
        data = {"title": "Попытка обновления"}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Редактирование запрещено', response.data['message'])
