from django.contrib import admin

from .models import Category, Kakeibo

admin.site.register(Category)
admin.site.register(Kakeibo)

class KakeiboAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'category', 'money', 'memo')
