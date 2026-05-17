from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Quiz.Status.PUBLISHED)


class Quiz(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='quizzes', verbose_name="Категория")
    tags = models.ManyToManyField('Tag', blank=True, related_name='quizzes', verbose_name="Теги")
    settings = models.OneToOneField('QuizSettings', on_delete=models.SET_NULL, null=True, blank=True, related_name='quiz',
                                    verbose_name="Детали теста ")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True, verbose_name="Фото")  # ← ПЕРЕНЕСЕНО
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='quizzes', null=True, default=None,
                               verbose_name="Автор")
    is_published = models.IntegerField(
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус"
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'quiz_slug': self.slug})


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название тега")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuizSettings(models.Model):
    time_limit = models.IntegerField(default=0, verbose_name="Время на прохождение (мин)")
    max_attempts = models.IntegerField(default=1, verbose_name="Максимум попыток")

    def __str__(self):
        return f"Настройки: {self.time_limit} мин, {self.max_attempts} попытки"

    class Meta:
        verbose_name = 'Детали теста'
        verbose_name_plural = 'Детали тестов'


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')