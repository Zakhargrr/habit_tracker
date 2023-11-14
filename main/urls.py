from django.urls import path

from main.apps import MainConfig
from main.views import HabitCreateAPIView, HabitListAPIView, HabitUpdateAPIView, HabitRetrieveAPIView, \
    HabitDestroyAPIView, PublicHabitListAPIView

app_name = MainConfig.name

urlpatterns = [
    path('create-habit/', HabitCreateAPIView.as_view(), name='create_habit'),
    path('my-habits/', HabitListAPIView.as_view(), name='my_habits'),
    path('my-habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='retrieve_habit'),
    path('update-habit/<int:pk>/', HabitUpdateAPIView.as_view(), name='update_habit'),
    path('delete-habit/<int:pk>/', HabitDestroyAPIView.as_view(), name='delete_habit'),
    path('public-habits/', PublicHabitListAPIView.as_view(), name='public_habits'),
]
