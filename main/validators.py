from rest_framework import serializers

from main.models import Habit


class ConHabitAndRewardValidator:
    def __init__(self, connected_habit, reward):
        self.connected_habit = connected_habit
        self.reward = reward

    def __call__(self, attrs):
        if self.connected_habit in attrs and self.reward in attrs:
            raise serializers.ValidationError("Указание связанной привычки и вознаграждения недопустимо")


class DurationValidator:
    def __init__(self, duration):
        self.duration = duration

    def __call__(self, attrs):
        if attrs[self.duration] > 120:
            raise serializers.ValidationError("Время выполнения привычки должно быть не больше 120 секунд")


class ConnectedHabitValidator:
    def __init__(self, connected_habit):
        self.connected_habit = connected_habit

    def __call__(self, attrs):
        if self.connected_habit in attrs:
            habit_to_check = Habit.objects.get(id=attrs[self.connected_habit].id)
            if not habit_to_check.is_pleasant_habit:
                raise serializers.ValidationError(
                    "В связанные привычки могут попадать только привычки с признаком приятной привычки")


class PleasantHabitValidator:
    def __init__(self, is_pleasant_habit, connected_habit, reward):
        self.is_pleasant_habit = is_pleasant_habit
        self.connected_habit = connected_habit
        self.reward = reward

    def __call__(self, attrs):
        if attrs[self.is_pleasant_habit]:
            if self.connected_habit in attrs or self.reward in attrs:
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки")


class PeriodValidator:
    period_arr = ["1D", "2D", "3D", "4D", "5D", "6D", "7D"]

    def __init__(self, period):
        self.period = period

    def __call__(self, attrs):
        if attrs[self.period] not in PeriodValidator.period_arr:
            raise serializers.ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")
