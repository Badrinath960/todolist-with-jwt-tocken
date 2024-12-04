from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-One link to the User model
    profile_image = models.ImageField(
        upload_to='profile_pics/',  # Directory to upload images
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],  # Valid file types
        blank=True
    )

    def __str__(self): 
        return self.user.username
