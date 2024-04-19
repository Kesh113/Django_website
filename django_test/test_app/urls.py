from django.urls import path, re_path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.TestAppHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('cats/<int:cat_id>/', views.categories, name='cats_id'),    # http://127.0.0.1:8000/cats/1
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),  # http://127.0.0.1:8000/cats/dda/
    #re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive),  # http://127.0.0.1:8000/archive/1993/
    path("archive/<year4:year>/", views.archive, name='archive'),   # http://127.0.0.1:8000/archive/1993/
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.TestAppCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.ShowTagPostList.as_view(), name='tag')
]
