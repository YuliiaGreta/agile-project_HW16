from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User
from apps.projects.models import Project  # Убедитесь, что эта модель существует и импортирована

class UserAPITests(TestCase):
    def setUp(self):
        # Устанавливаю клиент API и создаю двух тестовых пользователей
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='Str0ngP@ssw0rd!', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='Str0ngP@ssw0rd!', email='user2@example.com')

    def test_get_user_list(self):
        # Отправляю GET-запрос на получение списка пользователей
        response = self.client.get(reverse('user-list'))
        # Проверяю, что статус-код 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяю, что в ответе два пользователя
        self.assertEqual(len(response.data), 2)


class RegisterUserTests(TestCase):
    def setUp(self):
        # Устанавливаю клиент API
        self.client = APIClient()

    def test_register_user(self):
        # Данные для регистрации нового пользователя, включая обязательные поля
        data = {
            'username': 'newuser',
            'password': 'Str0ngP@ssw0rd!',  # Используем более сложный пароль
            're_password': 'Str0ngP@ssw0rd!',  # Подтверждение пароля
            'email': 'newuser@example.com',
            'first_name': 'New',  # Обязательное поле
            'last_name': 'User'  # Обязательное поле
        }
        # Отправляю POST-запрос на регистрацию пользователя
        response = self.client.post(reverse('user-register'), data)
        print(response.data)  # Выводим данные для отладки
        # Проверяем, что статус-код 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что пользователь создан
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_invalid_data(self):
        # Неверные данные для регистрации
        data = {
            'username': '',  # Пустое имя пользователя
            'password': 'password123',
            'email': 'invalid-email'
        }
        # Отправляю POST-запрос с неверными данными
        response = self.client.post(reverse('user-register'), data)
        # Проверяю, что статус-код 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserDetailAPITests(TestCase):
    def setUp(self):
        # Устанавливаю клиент API и создаю тестового пользователя
        self.client = APIClient()
        self.project = Project.objects.create(name='Agile Project')  # Создаю проект
        self.user = User.objects.create_user(
            username='testuser',
            password='Str0ngP@ssw0rd!',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            position='Developer',
            project=self.project  # Связываю пользователя с проектом
        )

    def test_get_user_detail(self):
        # Отправляю GET-запрос на получение информации о пользователе
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        # Проверяю, что статус-код 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяю, что данные пользователя в ответе соответствуют ожиданиям
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'john@example.com')

    def test_get_nonexistent_user_detail(self):
        # Отправляю GET-запрос с несуществующим ID
        response = self.client.get(reverse('user-detail', args=[999]))
        # Проверяю, что статус-код 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Проверяю, что в ответе содержится сообщение 'No User matches the given query.'
        self.assertEqual(response.data['detail'], 'No User matches the given query.')