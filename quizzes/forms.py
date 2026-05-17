from django import forms
from .models import Quiz, Category
from django.core.exceptions import ValidationError


class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="Категория не выбрана",
                                      label="Категория")

    class Meta:
        model = Quiz
        fields = ['title', 'slug', 'description', 'is_published', 'category', 'photo']
        labels = {
            'title': 'Заголовок',
            'slug': 'URL',
            'description': 'Описание',
            'is_published': 'Опубликовано',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 200:
            raise ValidationError('Длина описания превышает 200 символов')
        return description

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")