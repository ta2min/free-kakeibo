from accounts.models import CustomUser

from rest_framework import generics
from kakeibo.models import Kakeibo, Category
from .serializers import KakeiboSerializer, CategorySerializer


class KakeiboListCreateView(generics.ListCreateAPIView):
    """家計簿リスト表示・新規登録用API"""
    serializer_class = KakeiboSerializer

    def get_queryset(self):
        return Kakeibo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class KakeiboRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """詳細・更新・削除API"""
    serializer_class = KakeiboSerializer
    queryset = Kakeibo.objects.all()


class CategoryListCreateView(generics.ListCreateAPIView):
    """カテゴリリスト表示・新規登録用API"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """詳細・更新・削除API"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
