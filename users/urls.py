from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, \
    UserPaymentsAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('user/', UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-get'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('user/payments/', UserPaymentsAPIView.as_view(), name='user-payments'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
# {
#     "email": "admin@mail.ru",
#     "password": "Q1w2e3r4"
# }
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
#                ".eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTY5NzA2NCwiaWF0IjoxNjg5NjEwNjY0LCJqdGkiOiIxMzkxMjFlMTQyMDQ0OTI3YTZmMGY3ODRlMWQxMjRkYiIsInVzZXJfaWQiOjJ9.SzeTnaTHyYyvOpSNZjaOP-QQOvzAqCZHwJVg-tE__eQ",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
#               ".eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5NjEwOTY0LCJpYXQiOjE2ODk2MTA2NjQsImp0aSI6IjM2YTQ4MGJlMWIzZDQ4OTU4OGE5OTQ1NjM0NDYwOGUxIiwidXNlcl9pZCI6Mn0.du4w6XndbxULYJncYFAmNu8XU9m2VGxM0EdMHH7gPCk"
# }
