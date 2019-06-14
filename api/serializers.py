from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from kakeibo.models import Kakeibo, Category


class KakeiboSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kakeibo
        fields = ('id', 'date', 'category', 'money', 'memo')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'category_name', 'balance_label', 'user')
        validators = [
            # カテゴリ名とユーザがユニークになっていることをチェック
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=('category_name', 'user'),
                message="すでに登録されています"
            )
        ]