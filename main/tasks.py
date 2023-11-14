import os
from datetime import datetime, timedelta

from celery import shared_task
from notifiers import get_notifier

from main.models import Habit


def form_message(hours, minutes, action, duration, connected_habit, reward):
    if connected_habit:
        message = f"Напоминание: в {hours} часов и {minutes} минут вам нужно выполнить привычку '{action}' длительностью {duration} секунд.\n\nВ качестве награды выполните приятную привычку '{connected_habit.action}'."
    elif reward:
        message = f"Напоминание: в {hours} часов и {minutes} минут вам нужно выполнить привычку '{action}' длительностью {duration} секунд.\n\nВашей наградой за это будет {reward}."
    else:
        message = f"Напоминание: в {hours} часов и {minutes} минут вам нужно выполнить привычку '{action}' длительностью {duration} секунд."

    return message


@shared_task
def send_tg_message(chat_id, message):
    telegram = get_notifier('telegram')
    telegram.notify(token=os.getenv('TG_BOT_TOKEN'), chat_id=chat_id, message=message)


def check_time_and_timedelta(habit):
    if not habit.last_sending_datetime:
        now = datetime.now()
        time = now.time()

        if time > habit.time:
            message = form_message(habit.hours, habit.minutes, habit.action, habit.duration, habit.connected_habit,
                                   habit.reward)
            send_tg_message.delay(habit.user.chat_id, message)
            habit.last_sending_datetime = now
            habit.save()
    else:
        if habit.period == "1D":
            one_day = timedelta(days=1)
            now = datetime.now()
            habit_delta = now - habit.last_sending_datetime
            if habit_delta >= one_day:
                message = form_message(habit.hours, habit.minutes, habit.action, habit.duration, habit.connected_habit,
                                       habit.reward)
                send_tg_message.delay(habit.user.chat_id, message)
                habit.last_sending_datetime = now
                habit.save()

        elif habit.period == "2D":
            two_days = timedelta(days=2)
            now = datetime.now()
            habit_delta = now - habit.last_sending_datetime
            if habit_delta >= two_days:
                message = form_message(habit.hours, habit.minutes, habit.action, habit.duration, habit.connected_habit,
                                       habit.reward)
                send_tg_message.delay(habit.user.chat_id, message)
                habit.last_sending_datetime = now
                habit.save()

        elif habit.period == "3D":
            three_days = timedelta(days=3)
            now = datetime.now()
            habit_delta = now - habit.last_sending_datetime
            if habit_delta >= three_days:
                message = form_message(habit.hours, habit.minutes, habit.action, habit.duration, habit.connected_habit,
                                       habit.reward)
                send_tg_message.delay(habit.user.chat_id, message)
                habit.last_sending_datetime = now
                habit.save()

        elif habit.period == "4D":
            four_days = timedelta(days=4)
            now = datetime.now()
            habit_delta = now - habit.last_sending_datetime
            if habit_delta >= four_days:
                message = form_message(habit.hours, habit.minutes, habit.action, habit.duration, habit.connected_habit,
                                       habit.reward)
                send_tg_message.delay(habit.user.chat_id, message)
                habit.last_sending_datetime = now
                habit.save()

        elif habit.period == "5D":
            five_days = timedelta(days=5)
            now = datetime.now()
            habit_delta = now - habit.last_sending_datetime
            if habit_delta >= five_days:
                message = form_message(habit.hours, habit.minutes, habit.action, habit.duration, habit.connected_habit,
                                       habit.reward)
                send_tg_message.delay(habit.user.chat_id, message)
                habit.last_sending_datetime = now
                habit.save()

        elif habit.period == "6D":
            six_days = timedelta(days=6)
            now = datetime.now()
            habit_delta = now - habit.last_sending_datetime
            if habit_delta >= six_days:
                message = form_message(habit.hours, habit.minutes, habit.action, habit.duration, habit.connected_habit,
                                       habit.reward)
                send_tg_message.delay(habit.user.chat_id, message)
                habit.last_sending_datetime = now
                habit.save()

        elif habit.period == "7D":
            seven_days = timedelta(days=7)
            now = datetime.now()
            habit_delta = now - habit.last_sending_datetime
            if habit_delta >= seven_days:
                message = form_message(habit.hours, habit.minutes, habit.action, habit.duration, habit.connected_habit,
                                       habit.reward)
                send_tg_message.delay(habit.user.chat_id, message)
                habit.last_sending_datetime = now
                habit.save()


@shared_task
def check_time_to_send_message():
    habits = Habit.objects.all()
    for habit in habits:
        check_time_and_timedelta(habit)
