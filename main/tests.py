import datetime

from rest_framework.test import APITestCase

from main.models import Habit
from main.tasks import check_time_to_send_message
from users.models import User
from rest_framework import status


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create(
            email='test@mail.ru',
            first_name='Test',
            last_name='Test',
            is_staff=False,
            chat_id='213213'
        )
        self.client.force_authenticate(user)
        self.user = user

    def test_create_habit(self):
        habit1 = {
            'place': 'test_place',
            'hours': 10,
            'minutes': 50,
            'action': 'test_action',
            'is_pleasant_habit': False,
            'period': '1D',
            'reward': 'test_reward',
            'duration': 110,
        }

        response1 = self.client.post(
            '/create-habit/',
            data=habit1
        )

        self.assertEqual(
            response1.status_code,
            status.HTTP_201_CREATED
        )
        test_habit = {
            'place': 'test_place',
            'hours': 10,
            'minutes': 50,
            'action': 'test_action',
            'is_pleasant_habit': True,
            'period': '1D',
            'duration': 110,
        }
        self.client.post(
            '/create-habit/',
            data=test_habit
        )
        habit2 = {
            'place': 'test_place',
            'hours': 10,
            'minutes': 50,
            'action': 'test_action',
            'is_pleasant_habit': False,
            'connected_habit': Habit.objects.all().last(),
            'period': '1D',
            'reward': 'test_reward',
            'duration': 110,
        }
        response2 = self.client.post(
            '/create-habit/',
            data=habit2
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        habit3 = {
            'place': 'test_place',
            'hours': 10,
            'minutes': 50,
            'action': 'test_action',
            'is_pleasant_habit': True,
            'period': '1D',
            'reward': 'test_reward',
            'duration': 110,
        }
        response3 = self.client.post(
            '/create-habit/',
            data=habit3
        )

        self.assertEqual(
            response3.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        habit4 = {
            'place': 'test_place',
            'hours': 10,
            'minutes': 50,
            'action': 'test_action',
            'is_pleasant_habit': False,
            'period': '1D',
            'reward': 'test_reward',
            'duration': 130,
        }
        response4 = self.client.post(
            '/create-habit/',
            data=habit4
        )

        self.assertEqual(
            response4.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        habit5 = {
            'place': 'test_place',
            'hours': 10,
            'minutes': 50,
            'action': 'test_action',
            'is_pleasant_habit': False,
            'period': '9D',
            'reward': 'test_reward',
            'duration': 110,
        }
        response5 = self.client.post(
            '/create-habit/',
            data=habit5
        )

        self.assertEqual(
            response5.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_update_habit(self):
        test_habit = Habit.objects.create(place='test_place', hours=10, minutes=50, action='test_action',
                                          is_pleasant_habit=False, period='1D', reward='test_reward', duration=110,
                                          user=self.user)
        data = {
            'place': 'new_place',
            'hours': 10,
            'minutes': 50,
            'action': 'new_action',
            'is_pleasant_habit': False,
            'period': '1D',
            'reward': 'test_reward',
            'duration': 110,
        }
        response = self.client.put(
            f'/update-habit/{test_habit.pk}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()['place'],
            'new_place'
        )

        self.assertEqual(
            response.json()['action'],
            'new_action'
        )

    def test_list_habits(self):
        Habit.objects.create(place='test_place1', hours=10, minutes=50, action='test_action1',
                             is_pleasant_habit=False, period='1D', reward='test_reward1', duration=110,
                             user=self.user)
        Habit.objects.create(place='test_place2', hours=10, minutes=50, action='test_action2',
                             is_pleasant_habit=False, period='2D', reward='test_reward2', duration=110,
                             user=self.user)

        response = self.client.get(
            '/my-habits/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_check_time_to_send_message(self):
        Habit.objects.create(place='test_place1', hours=10, minutes=50, action='test_action1',
                             is_pleasant_habit=False, period='1D', reward='test_reward1', duration=110,
                             time=datetime.time(10, 50),
                             user=self.user)
        Habit.objects.create(place='test_place2', hours=10, minutes=50, action='test_action2',
                             is_pleasant_habit=False, period='2D', reward='test_reward2', duration=110,
                             time=datetime.time(10, 50),
                             user=self.user, last_sending_datetime=datetime.datetime.now())

        answer = check_time_to_send_message()
        self.assertEqual(
            answer,
            None
        )

    def test_retrieve_habit(self):
        habit = Habit.objects.create(place='test_place1', hours=10, minutes=50, action='test_action1',
                                     is_pleasant_habit=False, period='1D', reward='test_reward1', duration=110,
                                     user=self.user)

        response = self.client.get(
            f'/my-habits/{habit.pk}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()['place'],
            'test_place1'
        )

    def test_delete_habit(self):
        habit = Habit.objects.create(place='test_place1', hours=10, minutes=50, action='test_action1',
                                     is_pleasant_habit=False, period='1D', reward='test_reward1', duration=110,
                                     user=self.user)

        self.client.delete(
            f'/delete-habit/{habit.pk}/',
        )

        self.assertFalse(
            Habit.objects.all().exists()
        )

    def test_public_habits(self):
        Habit.objects.create(place='test_place1', hours=10, minutes=50, action='test_action1',
                             is_pleasant_habit=False, period='1D', reward='test_reward1', duration=110,
                             time=datetime.time(10, 50),
                             user=self.user, is_public=True)
        Habit.objects.create(place='test_place2', hours=10, minutes=50, action='test_action2',
                             is_pleasant_habit=False, period='2D', reward='test_reward2', duration=110,
                             time=datetime.time(10, 50),
                             user=self.user, is_public=True)

        response = self.client.get(
            '/public-habits/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertTrue(
            Habit.objects.all().exists()
        )
