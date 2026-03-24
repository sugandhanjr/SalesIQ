from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('BUSINESS_USER', 'Business User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='BUSINESS_USER')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in ₹")

    def __str__(self):
        return self.name


class SalesData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price at sale in ₹")
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    sale_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_revenue = self.quantity * self.sale_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} on {self.sale_date}"


class ForecastData(models.Model):
    prediction_date = models.DateField()
    predicted_sales = models.DecimalField(max_digits=12, decimal_places=2, help_text="Predicted revenue in ₹")
    confidence_score = models.FloatField(help_text="Confidence percentage (0-100)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Forecast for {self.prediction_date} - ₹{self.predicted_sales}"


class Insight(models.Model):
    explanation = models.TextField()
    influencing_factors = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.explanation[:50]


class Recommendation(models.Model):
    PRIORITY_CHOICES = (
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    )
    recommendation_text = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    generated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.priority}] {self.recommendation_text[:50]}"
