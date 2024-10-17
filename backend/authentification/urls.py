# authentification/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterView, CustomPasswordResetView, CustomPasswordResetConfirmView, UserProfileView, UserEditView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'authentification'  # Agrega esto para establecer un namespace


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentification/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentification/password_reset_complete.html'), name='password_reset_complete'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),  # Nueva URL para obtener el perfil
    path('user-edit/', UserEditView.as_view(), name='user-edit'),  # Nueva URL para editar el perfil
]

# Agrega esto si deseas manejar archivos multimedia en esta app
if settings.DEBUG:  # Asegúrate de que esto esté bajo la condición DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


