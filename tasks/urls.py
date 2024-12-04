from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('create/', views.task_create, name='task-create'),
    path('<int:pk>/update/', views.task_update, name='task-update'),
    path('<int:pk>/delete/', views.task_delete, name='task-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)