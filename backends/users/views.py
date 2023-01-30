from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import UserCreateSerializer, UserSerializer,UserLoginSerializer,UpdateUserSerializer
from django.contrib.auth import authenticate
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from .renderers import UserRenderer
from .models import UserAccount
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class RegisterView(APIView):
  def post(self, request):
    data = request.data

    serializer = UserCreateSerializer(data=data)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.create(serializer.validated_data)
    user = UserSerializer(user)

    return Response(user.data, status=status.HTTP_201_CREATED)


class RetrieveUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = request.user
    user = UserSerializer(user)

    return Response(user.data, status=status.HTTP_200_OK)


#sign in view
class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  serializer = UserLoginSerializer()
  def post(self, request, format=None):
    data = self.request.data
    email = data['email']
    password = data['password']
    try:
      user = authenticate(email=email, password=password)
      if user is not None:
          auth.login(request, user)
          token = get_tokens_for_user(user)
          return Response({ 'token':token,'success': 'User authenticated' })
      else:
          return Response({ 'error': 'Error Authenticating' })
    except:
      return Response({ 'error': 'Something went wrong when logging in' })
  

class UpdateProfileView(UpdateAPIView):

    queryset = UserAccount.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer