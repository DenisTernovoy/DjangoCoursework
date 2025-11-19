from django.urls import path
from users.apps import UsersConfig
from . import views

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("confirm-email/<str:token>/", views.confirm_email, name="confirm_email"),
    path(
        "login/",
        views.CustomLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        views.CustomLogoutView.as_view(),
        name="logout",
    ),
    path(
        "profile/<int:pk>/",
        views.CustomUserDetailView.as_view(),
        name="profile",
    ),
    path(
        "profile/<int:pk>/update/",
        views.CustomUserUpdateView.as_view(),
        name="profile_update",
    ),
    path(
        "password/reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("users/", views.UserListView.as_view(), name="users"),
    path("profile/<int:pk>/block/", views.block_user, name="block_user"),
    path("profile/<int:pk>/unblock/", views.unblock_user, name="unblock_user"),
]
