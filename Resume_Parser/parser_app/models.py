from django.db import models

# Create your models here.


# This model is used ti store the parsed resume data
class Parsed_Resume(models.Model):
    name = models.CharField(max_length = 100, null = True, blank = True)
    email = models.EmailField(max_length = 100, null = True, blank = True)
    phone = models.CharField(max_length = 15, null = True, blank = True)
    skills = models.TextField(null = True, blank = True)
    education = models.TextField(null = True, blank = True)
    experience = models.TextField(null = True, blank = True)
    projects = models.TextField(null = True, blank = True)
    certifications = models.TextField(null = True, blank = True)
    uploaded_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name or "Unknown Resume"

# This model is used to store temporary user data for OTP verification
class TempUser(models.Model):
    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    password = models.CharField(max_length=128, blank=False)
    otp = models.CharField(max_length=6, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    

