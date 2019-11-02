from django import forms
from django.utils import timezone
from .models import Kakeibo, Category, Family
from accounts.models import CustomUser


class KakeiboForm(forms.ModelForm):
    """家計簿データ登録・更新用フォーム"""

    class Meta:
        model = Kakeibo
        fields = ['date', 'category', 'money', 'memo']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        try:
            balance_label = kwargs.pop('balance_label')
        except KeyError:
            #  データ更新時はクエリパラメータ使う必要ないのでformから取り出す
            balance_label = kwargs['instance'].category.balance_label
        super(KakeiboForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = user.category_set.filter(balance_label=balance_label)


class CategoryForm(forms.ModelForm):
    """カテゴリ登録用フォーム"""
    
    class Meta:
        BALANCE_CHOICES = {
            (0, '支出'),
            (1, '収入'),
        } 
        model = Category
        fields = ['category_name', 'balance_label']
        widgets = {
            'balance_label': forms.RadioSelect(choices=BALANCE_CHOICES),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CategoryForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        print(self.user)
        user = self.user
        category_name = cleaned_data.get('category_name')

        if Category.check_duplicate(user, category_name):
            raise forms.ValidationError(f'{category_name}はすでに登録されています')
        return cleaned_data


class SelectYearAndMonthForm(forms.Form):
    """月次集計用フォーム"""
    BALANCE_LABEL_CHOICES = {
        (0, '支出'),
        (1, '収入')
    }
    now_year = timezone.now().year
    
    year_month = forms.DateField(label='年/月', widget=forms.SelectDateWidget(
        years=[x for x in range(now_year, now_year - 5, -1)]),
        initial = timezone.now)
    balance_label = forms.ChoiceField(widget=forms.Select, choices=BALANCE_LABEL_CHOICES)


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name']

class EmailForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')

    def clean(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('存在しないユーザのメールアドレスです。')
