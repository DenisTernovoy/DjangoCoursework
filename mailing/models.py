from django.db import models

from users.models import CustomUser


# Create your models here.
class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name="Email")
    name = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    avatar = models.ImageField(
        upload_to="mailing/photo", verbose_name="Аватар", null=True, blank=True
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email"]
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "email",
                    "owner",
                ),
                name="unique_client",
            )
        ]
        permissions = [
            ("can_watch_clients", "Can watch clients"),
        ]

    def __str__(self):
        return self.email


class Message(models.Model):
    title = models.CharField(max_length=120, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Тело письма")

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]

        permissions = [
            ("can_watch_messages", "Can watch messages"),
        ]

    def __str__(self):
        return self.title


class Mailing(models.Model):
    STATUSES = [
        ("created", "Создана"),
        ("active", "Запущена"),
        ("paused", "Остановлена"),
        ("stopped", "Завершена"),
    ]

    timestamp_start = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата и время первой отправки",
    )
    timestamp_end = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата и время последней отправки"
    )
    status = models.CharField(
        choices=STATUSES, verbose_name="Статус", default="created"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailings",
        null=True,
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status"]
        permissions = [
            ("can_pause_mailings", "Can pause mailings"),
            ("can_watch_mailings", "Can watch mailings"),
        ]

    def __str__(self):
        return self.message.title


class Attempt(models.Model):
    STATUSES = [
        (
            "ok",
            "Успешно",
        ),
        ("nok", "Не успешно"),
    ]
    datetime_attempt = models.DateTimeField(verbose_name="Дата и время попытки")
    status = models.CharField(choices=STATUSES, verbose_name="Статус")
    response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        Mailing, on_delete=models.SET_NULL, verbose_name="Рассылка", null=True
    )
    recipient = models.ForeignKey(
        Client, verbose_name="Получатели", on_delete=models.SET_NULL, null=True
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["-datetime_attempt"]

    def __str__(self):
        return str(self.mailing)
