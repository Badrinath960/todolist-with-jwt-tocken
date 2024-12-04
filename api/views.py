from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from tasks.models import Task
from users.models import Profile
from .serializers import UserSerializer, ProfileSerializer, LoginSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import login
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        # Check if the serializer data is valid
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'Some error occurred during registration.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Save the new user data
        serializer.save()

        # Retrieve the user to generate JWT tokens
        user = User.objects.get(username=serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        # Return the tokens and user info in the response
        return Response({
            'status': 200,
            'payload': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Your data is saved.'
        }, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)  # This will create a session
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)