from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('home/', views.home, name='home'),  # Home view mapped to the root of users' app.
    path('', views.details, name='details'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('logout-confirm/', views.logout_confirm, name='logout-confirm'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)