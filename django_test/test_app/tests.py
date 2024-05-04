from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from test_app.models import Test_app


class GetPagesTestCase(TestCase):
    fixtures = ['test_app_test_app.json', 'test_app_category.json', 'test_app_husband.json', 'test_app_tagpost.json']
    def setUp(self):
        pass
    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertIn('test_app/index.html', response.template_name)
        self.assertTemplateUsed(response, 'test_app/index.html')
        self.assertEqual(response.context_data['title'], "Главная страница")
    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        w = Test_app.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerysetEqual(response.context_data['posts'], w[:5])

    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        w = Test_app.published.all().select_related('cat')
        self.assertQuerysetEqual(response.context_data['posts'], w[(page - 1) * paginate_by:page * paginate_by])

    def test_content_post(self):
        w = Test_app.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)
    def tearDown(self):
        pass