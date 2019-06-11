from django.db import models
from django.utils import timezone

from accounts.models import CustomUser


class Category(models.Model):
    BALANCE_CHOICES = {
    (0, '支出'),
    (1, '収入'),
    }

    class Meta:
        db_table = 'category'
        unique_together = ('category_name', 'user')
     
    category_name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="ユーザ名")
    balance_label = models.IntegerField(verbose_name='収支ラベル', choices=BALANCE_CHOICES, default=0)

    @classmethod
    def check_duplicate(cls, user, category_name):
        return cls.objects.filter(user=user, category_name=category_name)
    
    def __str__(self):
        return self.category_name


class Kakeibo(models.Model):
    class Meta:
        db_table ='kakeibo'

    date = models.DateField(verbose_name='日付', default=timezone.now)
    category = models.ForeignKey(Category, on_delete = models.PROTECT, verbose_name='カテゴリ')
    money = models.IntegerField(verbose_name='金額', help_text='円')
    memo = models.CharField(verbose_name='メモ', max_length=500)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, verbose_name='ユーザ名')

    def __str__(self):
        return self.memo