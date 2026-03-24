from django.contrib import admin
from .models import UserProfile, Product, SalesData, ForecastData, Insight, Recommendation

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'category')
    list_filter = ('category',)

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'sale_price', 'total_revenue', 'sale_date')
    search_fields = ('product__name',)
    list_filter = ('sale_date', 'product__category')

@admin.register(ForecastData)
class ForecastDataAdmin(admin.ModelAdmin):
    list_display = ('prediction_date', 'predicted_sales', 'confidence_score', 'created_at')
    list_filter = ('prediction_date',)

@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ('explanation', 'influencing_factors', 'created_at')

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('recommendation_text', 'priority', 'generated_date')
    list_filter = ('priority',)
