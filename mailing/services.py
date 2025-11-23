import smtplib

from django.db.models import QuerySet
from config import settings
from config.settings import CACHE_ENABLED
from django.core.cache import cache

from mailing.models import Message


def send_simple_email(topic, message, recipient):
    sender_email = settings.EMAIL_HOST_USER
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_password = settings.EMAIL_HOST_PASSWORD

    # Сформируем заголовки письма
    message = f"Subject: {topic}\n\n{message}".encode("utf-8")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Устанавливаем защищенное соединение
            server.login(sender_email, smtp_password)
            server.sendmail(sender_email, recipient, message)  # Отправляем сообщение
        return "Сообщение успешно отправлено", "OK"
    except Exception as e:
        return str(e), "NOK"


def get_messages_list(owner) -> QuerySet:
    """Функция возвращает список всех продуктов в указанной категории"""

    if CACHE_ENABLED:
        data = cache.get(f"messages_of_{owner}")
        if data is None:
            messages = Message.objects.filter(owner=owner)
            cache.set(f"messages_of_{owner}", messages, 30)
            return messages

        return data

    return Message.objects.filter(owner=owner)
