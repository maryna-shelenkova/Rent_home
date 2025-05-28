from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Генерируем токены для нового пользователя
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Возвращаем в ответе данные пользователя и токены
            return Response({
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
                "refresh": refresh_token,
                "access": access_token,
            }, status=status.HTTP_201_CREATED)

        # Если данные невалидны — возвращаем ошибки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Профиль пользователя — вариант на базе RetrieveAPIView
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # Возвращаем текущего аутентифицированного пользователя
        return self.request.user


# Профиль пользователя — альтернативный вариант через APIView
class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)




