from django.urls import path

from . import views

app_name = 'kakeibo'

urlpatterns = [
    path('', views.KakeiboListView.as_view(), name='list'),
    path('add/', views.KakeiboCreateView.as_view(), name='add'),
    path('update/<int:pk>/', views.KakeiboUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.KakeiboDeleteView.as_view(), name='delete'),
    path('add_category', views.CategoryCreateView.as_view(), name='add_category'),
    path('circle/', views.CircleChartView.as_view(), name='kakeibo_circle'),
    path('transition_category', views.LineChartView.as_view(), name='kakeibo_line'),
    path('family/create', views.FamilyCreateView.as_view(), name='family_create'),
    path('family/add/', views.FamilyMemverCreateView.as_view(), name='family_member_create'),
    path('family/', views.KakeiboFamilyListView.as_view(), name='family_kakeibo'),
]