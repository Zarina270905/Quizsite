from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from datetime import date
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import Quiz, Category, Tag
from .forms import AddPostForm
from .forms import UploadFileForm
import uuid
from .models import UploadFiles
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Как это работает', 'url_name': 'how'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Нейросеть', 'url_name': 'gpt:ask'},
]


def index(request):
    quizzes = Quiz.published.all()
    context = {
        'title': 'Главная страница',
        'menu': menu,
        'tests': quizzes,  #
        'difficulty_stats': {'easy': 1, 'medium': 2, 'hard': 2},
        'cat_selected': 0,
        'hide_categories': False,
    }
    return render(request, 'quizzes/index.html', context)
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

@login_required
def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
            return redirect('about')
    else:
        form = UploadFileForm()

    return render(request, 'quizzes/about.html', {
        'title': 'О сайте',
        'menu': menu,
        'form': form,
        'hide_categories': False,
    })

def create_test(request):
    context = {
        'title': 'Создание теста',
        'menu': menu,
        'hide_categories': False,
    }
    return render(request, 'quizzes/create_test.html', context)

def how_it_works(request):
    context = {
        'title': 'Как это работает',
        'menu': menu,
        'steps': [
            'Зарегистрируйтесь на сайте',
            'Нажмите кнопку "Создать тест"',
            'Добавьте вопросы и ответы',
            'Опубликуйте тест',
            'Делитесь ссылкой с друзьями',
        ],
        'hide_categories': False,
    }
    return render(request, 'quizzes/how_it_work.html', context)

from django.http import HttpResponse

def test_detail(request, test_id):
    return HttpResponse(f"<h1>Тест</h1><p>ID теста: {test_id}</p>")


def category_tests(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    quizzes = Quiz.published.filter(category=category)

    context = {
        'title': f'Тесты: {category.name}',
        'menu': menu,
        'tests': quizzes,
        'categories': Category.objects.all(),
        'cat_selected': category.id,
        'hide_categories': False,
    }
    return render(request, 'quizzes/index.html', context)

def test_archive(request, year):
    if year > 2026:
        # Перенаправление на главную страницу (код 302 - временное)
        #return redirect('home')

        # Для постоянного перенаправления (код 301):
         return redirect('home', permanent=True)

    return HttpResponse(f"<h1>Архив тестов за {year} год</h1>")


def archive_redirect(request, year):
    if year > 2026:
        url_redirect = reverse('home')  # Получаем URL главной страницы
        return redirect(url_redirect)  # И делаем редирект

    return HttpResponse(f"<h1>Архив тестов за {year} год</h1>")
#def reverse_test(request):
    #url = reverse('create-test')
    #return HttpResponse(f"URL для создания теста: {url}")

#cats_db = [
   # {'id': 1, 'name': 'Программирование'},
    #{'id': 2, 'name': 'Веб-разработка'},
    #{'id': 3, 'name': 'Базы данных'},
    #{'id': 4, 'name': 'Алгоритмы'},
#]
def show_post(request, quiz_slug):
    post = get_object_or_404(Quiz, slug=quiz_slug, is_published=True)
    context = {
        'menu': menu,
        'post': post,
        'hide_categories': False,
    }
    return render(request, 'quizzes/post.html', context)

def show_tag_tests(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    quizzes = tag.quizzes.filter(is_published=Quiz.Status.PUBLISHED)

    context = {
        'title': f'Тег: {tag.name}',
        'menu': menu,
        'tests': quizzes,
        'categories': Category.objects.all(),
        'cat_selected': 0,
        'hide_categories': False,
    }
    return render(request, 'quizzes/index.html', context)


@login_required
@permission_required('quizzes.add_quiz', raise_exception=True)
def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            return redirect('home')
    else:
        form = AddPostForm()

    return render(request, 'quizzes/addpage.html', {
        'title': 'Добавление теста',
        'form': form,
        'menu': menu,
        'hide_categories': False,
    })

def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())

    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class UpdatePage(PermissionRequiredMixin, UpdateView):
    model = Quiz
    form_class = AddPostForm
    template_name = 'quizzes/updatepage.html'
    permission_required = 'quizzes.change_quiz'
    pk_url_kwarg = 'quiz_pk'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'quiz_slug': self.object.slug})

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.save()
        return super().form_valid(form)

@permission_required('quizzes.delete_quiz', raise_exception=True)
def delete_quiz(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    quiz.delete()
    return redirect('home')