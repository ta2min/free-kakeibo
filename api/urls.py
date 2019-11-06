from django.conf.urls import url
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    KakeiboListCreateView,
    KakeiboRetrieveUpdateDestroyView,
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
)


schema_view = get_schema_view(
   openapi.Info(
      title='Kakeibo API',
      default_version='v1',
      description='家計簿アプリのAPIドキュメント',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^documents/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('kakeibo/', KakeiboListCreateView.as_view()),
    path('kakeibo/<pk>/', KakeiboRetrieveUpdateDestroyView.as_view()),
    path('category/', CategoryListCreateView.as_view()),
    path('category/<pk>/', CategoryRetrieveUpdateDestroyView.as_view()),
]
