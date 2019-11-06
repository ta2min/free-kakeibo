from django.contrib import admin

from .models import Category, Kakeibo, Family, FamilyMember

admin.site.register(Category)
admin.site.register(Kakeibo)
admin.site.register(Family)
admin.site.register(FamilyMember)

class KakeiboAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'category', 'money', 'memo')
