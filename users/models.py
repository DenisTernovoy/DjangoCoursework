from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    nickname = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Никнейм"
    )
    avatar = models.ImageField(
        upload_to="users/avatar/", null=True, blank=True, verbose_name="Аватар"
    )
    phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Телефон"
    )
    country = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Страна"
    )

    token = models.CharField(max_length=32, null=True, blank=True, verbose_name="Токен")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_watch_users", "Can watch users"),
            ("can_block_users", "Can block users"),
        ]

    def __str__(self):
        return self.email
