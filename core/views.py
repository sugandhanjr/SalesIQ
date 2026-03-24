from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .forms import UserRegistrationForm, ProductForm, SalesDataForm
from .models import UserProfile, Product, SalesData, ForecastData, Insight, Recommendation
from .ml_pipeline import generate_forecasts

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user, role='BUSINESS_USER')
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('landing')

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def dashboard_view(request):
    total_sales = SalesData.objects.aggregate(t=Sum('total_revenue'))['t'] or 0
    recent_forecast = ForecastData.objects.order_by('-prediction_date').first()
    predicted_sales = recent_forecast.predicted_sales if recent_forecast else 0
    
    sales_data = SalesData.objects.all().order_by('-sale_date')[:10]
    insights = Insight.objects.order_by('-created_at')[:3]
    recommendations = Recommendation.objects.order_by('-generated_date')[:3]
    
    context = {
        'total_sales': total_sales,
        'predicted_sales': predicted_sales,
        'sales_data': sales_data,
        'insights': insights,
        'recommendations': recommendations
    }
    return render(request, 'dashboard.html', context)

@login_required
def trigger_forecast_view(request):
    try:
        generate_forecasts()
        messages.success(request, 'AI Forecasting completed successfully!')
    except Exception as e:
        messages.error(request, f'Error generating forecast: {str(e)}')
    return redirect('dashboard')

@login_required
def product_list(request):
    products = Product.objects.all().order_by('name')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products.html', {'products': products, 'form': form})

@login_required
def sales_list(request):
    sales = SalesData.objects.all().select_related('product')
    if request.method == 'POST':
        form = SalesDataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sales data recorded successfully.')
            return redirect('sales_list')
    else:
        form = SalesDataForm()
    return render(request, 'sales.html', {'sales': sales[:50], 'form': form})

@login_required
def forecast_view(request):
    forecasts = ForecastData.objects.all().order_by('prediction_date')
    recent_forecast = forecasts.last()
    predicted_sales = recent_forecast.predicted_sales if recent_forecast else 0
    
    context = {
        'forecasts': forecasts,
        'predicted_sales': predicted_sales,
        'forecasts_labels': [f.prediction_date.strftime('%b %d') for f in forecasts],
        'forecasts_data': [float(f.predicted_sales) for f in forecasts],
    }
    return render(request, 'forecast.html', context)

@login_required
def insights_view(request):
    insights = Insight.objects.all().order_by('-created_at')
    recommendations = Recommendation.objects.all().order_by('-generated_date')
    
    context = {
        'insights': insights,
        'recommendations': recommendations,
    }
    return render(request, 'insights.html', context)
