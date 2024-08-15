from django.urls import path
from djoser.views import UserViewSet
from djoser.views.authtoken import TokenCreateView, TokenDestroyView


urlpatterns = [
    path('auth/register/',
         UserViewSet.as_view({'post': 'create'}), name='custom_user_create'),
    path('auth/login/', TokenCreateView.as_view(), name='custom_user_login'),
    path('auth/logout/', TokenDestroyView.as_view(), name='custom_user_logout'),
]


"""
Если добавлять дополнительные ендпоинты из Djoser,
то можно подключить ихчерез DefaultRouter

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns += router.urls
"""
