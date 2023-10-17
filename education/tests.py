from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework.authtoken.models import Token
from .serializers import LessonSerializer
from django.urls import reverse
from rest_framework import status
from users.models import User
from education.models import Course, Lesson, Subscription


class LessonAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', email='user@test.com', password='test123456')
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        force_authenticate(self.client, user=self.user, token=self.token)
        self.course = Course.objects.create(title='Test Course')
        self.lesson = Lesson.objects.create(course=self.course, title='Test Lesson', description='Lesson Description', owner=self.user)
        self.url = reverse('education:lesson-retrieve-update-destroy', args=[self.lesson.id])
        self.subscribe_url = reverse('education:subscribe_to_course', args=[self.course.id])

    def test_get_lesson(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson_serializer = LessonSerializer(self.lesson)
        self.assertEqual(response.data, lesson_serializer.data)

    def test_update_lesson(self):
        updated_data = {'title': 'Updated Lesson Title', 'description': 'Updated Lesson Description'}
        response = self.client.patch(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, updated_data['title'])
        self.assertEqual(self.lesson.description, updated_data['description'])

    def test_delete_lesson(self):
        # url = f'/api/lessons/{self.lesson.id}/'
        print("URL for DELETE request:", self.url)
        response = self.client.delete(self.url, args=[self.lesson.pk])
        # response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Lesson.DoesNotExist):
            self.lesson.refresh_from_db()

    def test_subscribe_to_course(self):
        headers = {'Authorization': 'Token {}'.format(self.token.key)}
        response = self.client.post(self.subscribe_url, headers=headers)
        # Проверяем, что подписка была успешно создана
        self.assertEqual(response.status_code, 201)
        subscription = Subscription.objects.get(user=self.user, course=self.course)
        self.assertIsNotNone(subscription)
        # self.client.force_authenticate(user=self.user)  # Аутентифицировать пользователя
        # response = self.client.post(self.subscribe_url, data={})
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsubscribe_from_course(self):
        headers = {'Authorization': 'Token {}'.format(self.token.key)}
        response = self.client.post(self.subscribe_url, headers=headers)
        # Отписываем пользователя от курса
        unsubscribe_url = reverse('education:unsubscribe_from_course', args=[self.course.id])
        response = self.client.post(unsubscribe_url, headers=headers)
        # Проверяем, что подписка была успешно удалена
        self.assertEqual(response.status_code, 204)  # 204 - No Content
        # Проверяем, что подписка больше не существует
        with self.assertRaises(Subscription.DoesNotExist):
            Subscription.objects.get(user=self.user, course=self.course)













