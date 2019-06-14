from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kakeibo.models import Kakeibo, Category


class TestKakeiboListView(TestCase):
    """KakeiboListViewのテスト"""

    def setUp(self):
        print("# {} is running!".format(self.id()))
        # データベースに登録済みのユーザーを self.user にセット
        self.user = get_user_model().objects.create_user(
            username='test', email='test', password='pass')
        self.client.login(username=self.user.username, password='pass')

    def test_get(self):
        """"/kakeibo へのGETリクエストすると
        からのkakeibo_listが来ることを検証"""
        response = self.client.get(reverse('kakeibo:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['kakeibo_list'], [])

    def test_1post_and_get(self):
        """データを１件追加し、GETアクセスの結果を検証"""
        category = Category.objects.create(category_name="交通費", balance_label=0, user=self.user)
        kakeibo = Kakeibo.objects.create(category=category, money=1000, memo="電車", user=self.user)
        response = self.client.get(reverse('kakeibo:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['kakeibo_list'], ['<Kakeibo: 電車>'])
        self.assertContains(response, kakeibo.memo)


class TestCreateView(TestCase):
    """KakeiboCreateViewのテスト"""

    def setUp(self):
        print("# {} is running!".format(self.id()))
        # データベースに登録済みのユーザーを self.user にセット
        self.user = get_user_model().objects.create_user(
            username='test', email='test', password='pass')
        self.client.login(username=self.user.username, password='pass')

    def test_get(self):
        """"/kakeibo/add/?balance_label=0 へのGETリクエスト検証"""
        response = self.client.get(reverse('kakeibo:add'), {'balance_label': 0})
        self.assertEqual(response.status_code, 200)
        # self.assertQuerysetEqual(response.context['kakeibo_list'], [])


class TestUpdateView(TestCase):
    """KakeiboUpdateViewのテスト"""

    def setUp(self):
        print("# {} is running!".format(self.id()))
        # データベースに登録済みのユーザーを self.user にセット
        self.user = get_user_model().objects.create_user(
            username='test', email='test', password='pass')
        self.client.login(username=self.user.username, password='pass')
        self.category = Category.objects.create(category_name="交通費", balance_label=0, user=self.user)
        self.kakeibo = Kakeibo.objects.create(category=self.category, money=1000, memo="電車", user=self.user)

    def test_get(self):
        """/kakeibo/update/1/ のGETアクセス検証"""
        response = self.client.get(reverse('kakeibo:update', kwargs={'pk': self.kakeibo.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.kakeibo.memo)

    # def test_post(self):
    #     response = self.client.post(reverse('kakeibo:update', kwargs={'pk': self.kakeibo.id}), {
    #         'date': '2019-6-12',
    #         'category': '交通費',
    #         'money': 1000,
    #         'memo': 'バス',
    #     })
    #     print(response.context['form'])
    #     self.assertRedirects(response, reverse('kakeibo:list'))
    #     self.assertTrue(Kakeibo.objects.filter(memo='バス').exists())


class TestDeleteView(TestCase):
    """KakeiboUpdateViewのテスト"""

    def setUp(self):
        print("# {} is running!".format(self.id()))
        # データベースに登録済みのユーザーを self.user にセット
        self.user = get_user_model().objects.create_user(
            username='test', email='test', password='pass')
        self.client.login(username=self.user.username, password='pass')
        self.category = Category.objects.create(category_name="交通費", balance_label=0, user=self.user)
        self.kakeibo = Kakeibo.objects.create(category=self.category, money=1000, memo="電車", user=self.user)

    def test_get(self):
        response = self.client.get(reverse('kakeibo:delete', kwargs={'pk': self.kakeibo.id}))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """データが削除できることを検証"""
        response = self.client.post(reverse('kakeibo:delete', kwargs={'pk': self.kakeibo.id}))
        self.assertRedirects(response, reverse('kakeibo:list'))
        self.assertFalse(Kakeibo.objects.filter(pk=self.kakeibo.id).exists())


class TestCategoryCreateView(TestCase):
    """CategoryCreateViewのテスト"""

    def setUp(self):
        print("# {} is running!".format(self.id()))
        # データベースに登録済みのユーザーを self.user にセット
        self.user = get_user_model().objects.create_user(
            username='test', email='test', password='pass')
        self.client.login(username=self.user.username, password='pass')
        self.category = Category.objects.create(category_name="交通費", balance_label=0, user=self.user)

    def test_get(self):
        response = self.client.get(reverse('kakeibo:add_category'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """カテゴリが登録できることを確認"""
        response = self.client.post(reverse('kakeibo:add_category'), {
            'category_name': '食費',
            'balance_label': 0,
        })
        self.assertRedirects(response, reverse('kakeibo:list'))
        self.assertTrue(Category.objects.filter(pk=2).exists())



class TestCircleChartView(TestCase):
    def setUp(self):
        print("# {} is running!".format(self.id()))
        # データベースに登録済みのユーザーを self.user にセット
        self.user = get_user_model().objects.create_user(
            username='test', email='test', password='pass')
        self.client.login(username=self.user.username, password='pass')
        self.category = Category.objects.create(category_name="交通費", balance_label=0, user=self.user)
        self.category2 = Category.objects.create(category_name="食費", balance_label=0, user=self.user)
        self.kakeibo = Kakeibo.objects.create(category=self.category, money=1000, memo="電車", user=self.user)
        self.kakeibo2 = Kakeibo.objects.create(category=self.category2, money=1000, memo="ランチ", user=self.user)

    def test_get(self):
        """今月の円グラフのデータ検証"""
        response = self.client.get(reverse('kakeibo:kakeibo_circle'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category_dict'], {'食費': 50, '交通費': 50})