from rest_framework import serializers
from django.contrib.auth.models import User
from tasks.models import Task
from users.models import Profile
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def create(self, validated_data):
        # Extract the password
        password = validated_data.pop('password')

        # Create the user instance without the password first
        user = User(**validated_data)

        # Hash the password using set_password
        user.set_password(password)

        # Save the user with the hashed password
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Read-only for user field

    class Meta:
        model = Profile
        fields = ['user', 'image']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials, please try again.")

        data['user'] = user
        return data


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'user']
        read_only_fields = ['user']