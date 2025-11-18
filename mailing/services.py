import smtplib
from django.core.mail import send_mail
from config import settings


def send_mail_with_report(subject, message, from_email, to_email):
    try:
        # Создаем SMTP объект
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()  # Начинаем TLS
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Отправка письма
        response = server.send_mail(settings.EMAIL_HOST_USER, recipient_list, message)

        # Закрываем соединение
        server.quit()

        return response  # Здесь будет ответ сервера

    except Exception as e:
        return str(e)  # В случае ошибки возвращаем текст ошибки
