from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,UserManager 
from django.db import models
from django.utils import timezone
from datetime import datetime



# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='',unique=True)
    name= models.CharField(max_length=255, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_fill_name(self):
        return self.name or self.email.split('@')[0]
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    club = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    year = models.IntegerField()
    image_link = models.CharField(max_length=5000)
    price = models.FloatField() 
    
    def __str__(self):
        return f"{self.club}, {self.league}, {self.year}"

class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_cart")
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.owner}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="in_cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="in_cart_item")
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=32)


    def __str__(self):
        return f"{self.product} x{self.quantity} is in the cart"

class PastOrder(models.Model):
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_order")
    ordered_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.owner}'s order"

class OrderItem(models.Model):
    pastOrder = models.ForeignKey(PastOrder, on_delete=models.CASCADE, related_name="in_order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="in_order_item")
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=32)
    ordered_at = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return f"{self.product} x{self.quantity} was ordered"
    
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_reviews")
    content = models.CharField(max_length=50000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products_reviews")
    rating = models.IntegerField(default=4)
    written_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.product} was give a {self.rating} star review by {self.author}"
