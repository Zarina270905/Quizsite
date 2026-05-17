from django.contrib import admin
from django.urls import path, include
from quizzes import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Панель администрирования Quizsite"
admin.site.index_title = "Управление тестами и вопросами"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quizzes/', include('quizzes.urls')),
    path('archive/<int:year>/', views.test_archive, name='test-archive'),
    path('', views.index, name='home'),
    path('users/', include('users.urls', namespace="users")),
    path('maps/', include('maps.urls', namespace="maps")),
    path('gpt/', include('gpt.urls', namespace='gpt')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Обработчик 404
handler404 = views.page_not_found