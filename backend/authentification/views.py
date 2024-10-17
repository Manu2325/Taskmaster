# authentification/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator



User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = []

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    email_template_name = 'authentification/password_reset_email.html'
    success_message = "Se ha enviado un enlace de recuperación de contraseña a su correo electrónico."
    success_url = reverse_lazy('authentification:password_reset_done')
    template_name = 'authentification/password_reset.html'

class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    success_message = "¡Su contraseña ha sido restablecida con éxito!"
    success_url = reverse_lazy('authentification:password_reset_complete')
    template_name = 'authentification/password_reset_confirm.html'

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        user = request.user
        # Aquí puedes devolver la información del perfil del usuario
        return Response({
            'username': user.username,
            'nombre': user.nombre,
            'email': user.email,
            'apellido': user.apellido,
            'direccion': user.direccion,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,  # Agrega la URL de la foto de perfil
        })


class UserEditView(APIView):
    def put(self, request):
        user = request.user
        print(request.data)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)