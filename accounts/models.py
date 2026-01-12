from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserManager(models.Manager):
    def create_user(self, username, email, password, user_type, name, phone=None):
        user = self.model(
            username=username,
            email=email,
            user_type=user_type,
            name=name,
            phone=phone
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class UserProfile(models.Model):
    USER_TYPE_CHOICES = (('patient', 'Patient'), ('doctor', 'Doctor'))

    username = models.CharField(max_length=150, unique=True)
    current_role = models.CharField(max_length=20, choices=[("doctor","Doctor"),("patient","Patient")], default="patient")
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=256)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    license = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    blood_group = models.CharField(max_length=3, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visit_fee = models.CharField(max_length=50, blank=True, null=True)

    objects = UserManager()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.user_type})"
