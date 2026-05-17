from django.contrib import admin, messages
from .models import Category, Quiz, Question, Answer, Tag, QuizSettings
from django.utils.safestring import mark_safe

class HasTagsFilter(admin.SimpleListFilter):
    title = 'Наличие тегов'
    parameter_name = 'has_tags'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Есть теги'),
            ('no', 'Нет тегов'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(tags__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(tags__isnull=True)
        return queryset

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    @admin.action(description="Опубликовать выбранные тесты")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Quiz.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} тестов(а).")

    @admin.action(description="Снять с публикации выбранные тесты")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Quiz.Status.DRAFT)
        self.message_user(request, f"{count} тестов(а) сняты с публикации!", messages.WARNING)

    list_display = ('id', 'title', 'time_create', 'is_published', 'category', 'post_photo')
    list_display_links = ('id', 'title')
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 5
    actions = [set_published, set_draft]
    search_fields = ['title', 'category__name']
    list_filter = ['category__name', 'is_published', HasTagsFilter]
    fields = ['title', 'slug', 'description', 'category', 'is_published', 'tags', 'photo', 'post_photo']
    readonly_fields = ['post_photo']
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description="Краткая информация")
    def brief_info(self, quiz: Quiz):
        return f"Описание: {len(quiz.description)} символов, вопросов: {quiz.question_set.count()}"

    @admin.display(description="Изображение")
    def post_photo(self, quiz: Quiz):
        if quiz.photo:
            return mark_safe(f'<img src="{quiz.photo.url}" width="50" height="50">')
        return "Нет фото"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'text')
    list_display_links = ('id', 'text')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')
    list_display_links = ('id', 'text')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')

@admin.register(QuizSettings)
class QuizSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_limit', 'max_attempts')
    list_display_links = ('id',)

