import calendar
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    FormView,
    View,
)
from accounts.models import CustomUser
from kakeibo.models import Category, Kakeibo, Family, FamilyMember
from .forms import (
    KakeiboForm,
    CategoryForm,
    SelectYearAndMonthForm,
    FamilyForm,
    EmailForm,
)

EXPENSE = 0


class KakeiboListView(LoginRequiredMixin, ListView):
    model = Kakeibo

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = user.kakeibo_set.select_related('category')
        context = {
            'kakeibo_list': queryset,
        }
        return render(request, 'kakeibo/kakeibo_list.html', context)


class KakeiboCreateView(LoginRequiredMixin, CreateView):
    model = Kakeibo
    form_class = KakeiboForm
    success_url = reverse_lazy('kakeibo:list')
    template_name = 'kakeibo/kakeibo_edit.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(KakeiboCreateView, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super(KakeiboCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if 'balance_label' in self.request.GET:
            kwargs['balance_label'] = self.request.GET.get('balance_label')
        else:
            print(kwargs)
        return kwargs


class KakeiboUpdateView(LoginRequiredMixin, UpdateView):
    model = Kakeibo
    form_class = KakeiboForm
    success_url = reverse_lazy('kakeibo:list')
    template_name = 'kakeibo/kakeibo_edit.html'

    def get_form_kwargs(self):
        kwargs = super(KakeiboUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class KakeiboDeleteView(LoginRequiredMixin, DeleteView):
    model = Kakeibo
    success_url = reverse_lazy('kakeibo:list')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('kakeibo:list')
    template_name = 'kakeibo/category_edit.html'

    def get_form_kwargs(self):
        kwargs = super(CategoryCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CategoryCreateView, self).form_valid(form)
    

class CircleChartView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        first_date, last_date = self.get_month_first_and_last_date(timezone.now().year, timezone.now().month)
        current_month_kakeibo_list = user.kakeibo_set.select_related('category').filter(category__balance_label=EXPENSE, date__range=(first_date, last_date)
                                                            ).order_by('-date')

        total = sum([item.money for item in current_month_kakeibo_list])
        
        category_data = user.category_set.filter(balance_label=EXPENSE)
        
        categories_name = [item.category_name for item in category_data]
        
        category_dict = self.get_category_ratio(categories_name, total, current_month_kakeibo_list)
        form = SelectYearAndMonthForm()
        context = {
            'category_dict': category_dict,
            'kakeibo_list': current_month_kakeibo_list,
            'form': form,
        }
        
        return render(request, 'kakeibo/circle_chart.html', context)

    def post(self, request, *args, **kwargs):
        form = SelectYearAndMonthForm(request.POST)

        if not form.is_valid():
            return render(request, 'kakeibo/circle_chart.html', {'form': form})
        user = self.request.user
        date = form.cleaned_data.get('year_month')
        balance_label = form.cleaned_data.get('balance_label')
        first_date, last_date = self.get_month_first_and_last_date(date.year, date.month)
        month_kakeibo_list = user.kakeibo_set.filter(date__range=(first_date, last_date),
                                    category__balance_label=form.cleaned_data.get('balance_label')).order_by('-date')

        total = sum([item.money for item in month_kakeibo_list])
        
        category_data = user.category_set.filter(balance_label=balance_label)
        categories_name = [item.category_name for item in category_data]
        category_dict = self.get_category_ratio(categories_name, total, month_kakeibo_list)
        
        context = {
            'category_dict': category_dict,
            'kakeibo_list': month_kakeibo_list,
            'form': form,
        }
        return render(request, 'kakeibo/circle_chart.html', context)
    
    def get_month_first_and_last_date(self, year, month):
        month_last_day = calendar.monthrange(int(year), int(month))[1]
        return (f'{year}-{month}-01', f'{year}-{month}-{month_last_day}')
    
    def get_category_ratio(self, categories_name, total, kakeibo_list):
        category_dict = {}
        for item in categories_name:
            category_total = kakeibo_list.filter(category__category_name=item
                                            ).aggregate(sum=models.Sum('money'))['sum']
            if category_total is not None:
                ratio = int((category_total / total) * 100)
                category_dict[item] = ratio
            else:
                ratio = 0
                category_dict[item] = ratio
        return category_dict


class LineChartView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = self.request.user
        kakeibo_data = user.kakeibo_set.filter(category__balance_label=EXPENSE)
        category_data = user.category_set.filter(balance_label=EXPENSE).order_by('-category_name')
        category_list = [item.category_name for item in category_data]
        date_list = [item.date.strftime('%Y/%m') for item in kakeibo_data]
        x_label = sorted(list(set(date_list)))
        monthly_total_data = []
        for date in x_label:
            year, month = date.split('/')
            month_last_day = calendar.monthrange(int(year), int(month))[1]
            first_date = f'{year}-{month}-01'
            last_date = f'{year}-{month}-{month_last_day}'
            #  1ヶ月分データ取得
            total_of_month = kakeibo_data.filter(date__range=(first_date, last_date))
            categories_total = total_of_month.values('category').annotate(total_price=models.Sum('money'))

            for category_total in categories_total:
                money = category_total['total_price']
                category = Category.objects.get(pk=category_total['category'])
                monthly_total_data.append([date, category.category_name, money])
        """
        月のカテゴリの合計金額が0の場合はcategories_totalには値が入っていないので
        0埋めしたmatrix_listに上書きしていく
        """
        matrix_list =[]
        for item_label in x_label:
            for item_category in category_list:
                matrix_list.append([item_label, item_category, 0])

        for yyyy_mm,category,total in monthly_total_data:
            for i,data in enumerate(matrix_list):
                if data[0] == yyyy_mm and data[1] == category:
                    matrix_list[i][2] = total
        context = {
            'x_label': x_label,
            'category_list': category_list,
            'matrix_list': matrix_list,
        }

        return render(request, 'kakeibo/line_chart.html', context)


class FamilyCreateView(LoginRequiredMixin, CreateView):
    model = Family
    form_class = FamilyForm
    success_url = reverse_lazy('kakeibo:family_member_create')
    template_name = 'kakeibo/family_edit.html'

    def form_valid(self, form):
        family = form.save()
        FamilyMember.objects.create(family_id=family, member=self.request.user)
        return redirect('kakeibo:family_member_create')


class FamilyMemverCreateView(LoginRequiredMixin, FormView):
    form_class = EmailForm
    template_name = 'kakeibo/family_member_invitation.html'
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        add_member = CustomUser.objects.get(email=email)
        family_id = FamilyMember.objects.get(member=self.request.user).family_id
        FamilyMember.objects.create(family_id=family_id, member=add_member)

        if 'save_and_add' in self.request.POST:
            return redirect('kakeibo:family_member_create')
        
        return redirect('kakeibo:list')

    
class KakeiboFamilyListView(LoginRequiredMixin, ListView):
    model = Kakeibo

    def get(self, request, *args, **kwargs):
        user = self.request.user
        family_members = FamilyMember.objects.filter(family_id=user.familymember_set.get().family_id)
        q_family_members = models.Q()
        for member in family_members:
            q_family_members |= models.Q(user=member.member)
        family_kakeibo = Kakeibo.objects.filter(q_family_members)
        context = {
            'kakeibo_list': family_kakeibo,
            'user_display': True,
        }
        return render(request, 'kakeibo/kakeibo_list.html', context)