import datetime

from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from main.models import Habit
from main.paginators import CustomPaginator
from main.permissions import IsOwner
from main.serializers import CreateHabitSerializer, ViewHabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user

        new_habit.time = datetime.time(new_habit.hours, new_habit.minutes)
        new_habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CreateHabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ViewHabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitListAPIView(generics.ListAPIView):
    serializer_class = ViewHabitSerializer

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user)

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPaginator


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = ViewHabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPaginator