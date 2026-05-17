from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('create/', views.create_test, name='create-test'),
    path('how/', views.how_it_works, name='how'),
    path('test/<int:test_id>/', views.test_detail, name='test-detail'),
    path('test/<slug:quiz_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.category_tests, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_tests, name='tag'),
    path('addpage/', views.addpage, name='addpage'),
    path('edit/<int:quiz_pk>/', views.UpdatePage.as_view(), name='update_page'),
    path('delete/<int:quiz_pk>/', views.delete_quiz, name='delete_quiz'),
]