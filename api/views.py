from accounts.models import CustomUser

from rest_framework import generics
from kakeibo.models import Kakeibo, Category
from .serializers import KakeiboSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework import status


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
    
    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """詳細・更新・削除API"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
