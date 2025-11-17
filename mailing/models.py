from django.db import models


# Create your models here.
class Client(models.Model):
    email = models.EmailField(unique=True, max_length=100, verbose_name="Email")
    name = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    avatar = models.ImageField(
        upload_to="mailing/photo", verbose_name="Аватар", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email"]

    def __str__(self):
        return self.email


class Message(models.Model):
    title = models.CharField(max_length=120, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Тело письма")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Mailing(models.Model):
    STATUSES = [
        ("created", "Создана"),
        ("active", "Запущена"),
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
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status"]

    def __str__(self):
        return self.message.title


class Attempt(models.Model):
    statuses = [
        (
            "ok",
            "Успешно",
        ),
        ("nok", "Не успешно"),
    ]
    datetime_attempt = models.DateTimeField(verbose_name="Дата и время попытки")
    status = models.CharField(choices=statuses, verbose_name="Статус")
    response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["-datetime_attempt"]

    def __str__(self):
        return self.mailing
