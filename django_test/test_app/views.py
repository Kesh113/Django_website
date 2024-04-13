from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .forms import AddPostForm, UploadFileForm
from .models import Test_app, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]
class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_info(self):
        return self.a + self.b

def index(request):
    # t = render_to_string('test_app/index.html')
    # return HttpResponse(t)
    posts = Test_app.published.all().select_related('cat')
    data = {
        'title': 'главная страница',
        'menu': menu,
        'float': 28.56,
        'lst': [1, 2, 'abc', True],
        'set': {1, 2, 3, 2, 5},
        'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
        'obj': MyClass(10, 20),
        'url': slugify("The main page"),
        'posts': posts,
        'cat_selected': 0,
                 }
    return render(request, 'test_app/index.html', context=data)

def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    return render(request, 'test_app/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})
def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи категории</h1><p>id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи категории</h1><p>slug: {cat_slug}</p>")

def archive(request, year):
    if year > 2023:
        uri = reverse('cats', args=('music', ))
        return redirect(uri)
    return HttpResponse(f"<h1>архив по годам</h1><p>{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")

def show_post(request, post_slug):
    post = get_object_or_404(Test_app, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'test_app/post.html', data)

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # try:
            #     Test_app.objects.create(**form.cleaned_data)
            #     return redirect("home")
            # except:
            #     form.add_error(None, "Ошибка добавления поста")
            form.save()
            return redirect("home")
    else:
        form = AddPostForm()
    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form,
    }
    return render(request, 'test_app/addpage.html', data)

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Test_app.published.filter(cat_id=category.pk).select_related("cat")
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'test_app/index.html', context=data)

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Test_app.Status.PUBLISHED).select_related("cat")

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None
    }

    return render(request, 'test_app/index.html', context=data)