from django.urls import path
from .views import (
    KakeiboListCreateView,
    KakeiboRetrieveUpdateDestroyView,
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('kakeibo/', KakeiboListCreateView.as_view()),
    path('kakeibo/<pk>/', KakeiboRetrieveUpdateDestroyView.as_view()),
    path('category/', CategoryListCreateView.as_view()),
    path('category/<pk>/', CategoryRetrieveUpdateDestroyView.as_view()),
]
