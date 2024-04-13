from django import forms
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Test_app
from django.core.validators import MinLengthValidator, MaxLengthValidator, ValidationError

@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)

class AddPostForm(forms.ModelForm):
    # title = forms.CharField(min_length=5, max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         error_messages={'min_length': 'Слишком короткий заголовок', 'required': 'Без заголовка никак'},
    #                         validators=[
    #                             RussianValidator(),
    #                         ])
    # slug = forms.SlugField(max_length=255, label="URL", validators=[
    #     MinLengthValidator(5, message="Минимум 5 символов"),
    #     MaxLengthValidator(100, "Максимум 100 символов"),
    # ])
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    # is_published = forms.BooleanField(required=False, initial=True, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем", label="Муж")

    class Meta:
        model = Test_app
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})}
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return title

class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')