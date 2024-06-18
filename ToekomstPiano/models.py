from django.db import models


class UserRegistration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # Storing hashed password as string
    password = models.CharField(max_length=255)
    # Making date of birth optional
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.email

class InviteCode(models.Model):
    email = models.EmailField(unique=True)
    invite_code = models.CharField(max_length=20)
    # Add any other fields you want to include in the invite code model

    def __str__(self):
        return self.email

class ThemePreference(models.Model):
    LIGHT = 'light'
    DARK = 'dark'
    THEME_CHOICES = [
        (LIGHT, 'Light'),
        (DARK, 'Dark'),
    ]
    email = models.EmailField(primary_key=True)
    theme_preference = models.CharField(max_length=5, choices=THEME_CHOICES)

    def __str__(self):
        return self.email
# models.py
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Payment(models.Model):
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class ProfileSettingsForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    state_region = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class ExperienceForm(models.Model):
    email = models.EmailField()
    designing_experience = models.CharField(max_length=255)
    additional_details = models.TextField()

    def __str__(self):
        return self.email
