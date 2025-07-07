import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def admin(request):
    from django.contrib import admin
    return admin.site.urls

def home(request):
    return render(request, "home.html")

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def chart(request):
    return render(request, "chart.html")

@login_required
def portfolio(request):
    return render(request, "portfolio.html")

@login_required
def announcement(request):
    return render(request, "announcement.html")

@login_required
def payment(request):
    return render(request, "payment.html")

@login_required
def prediction(request):
    data_dir = os.path.join(BASE_DIR, 'data')
    stock_list = [f.replace('.json', '') for f in os.listdir(data_dir) if f.endswith('.json')]

    predicted_ltp_path = os.path.join(BASE_DIR, 'prediction', 'predicted_ltp.json')
    try:
        with open(predicted_ltp_path) as f:
            predicted_ltp_data = json.load(f)
        print(f"Loaded predicted_ltp.json successfully. Keys: {list(predicted_ltp_data.keys())[:5]}")
    except Exception as e:
        print(f"Error loading predicted_ltp.json: {e}")
        predicted_ltp_data = {}

    selected_stock = request.GET.get('stock')
    predicted_price = None
    actual_prices = []
    prediction_plot = None

    if selected_stock:
        try:
            data_path = os.path.join(data_dir, f"{selected_stock}.json")
            with open(data_path) as f:
                historical_data = json.load(f)

            prices = [entry["LTP"] for entry in historical_data if "LTP" in entry]
            actual_prices = prices
            predicted_price = predicted_ltp_data.get(selected_stock.lower())

            plot_filename = f"{selected_stock.lower()}.png"
            prediction_plot = os.path.join('plots', plot_filename)

        except Exception as e:
            print(f"Error processing stock {selected_stock}: {e}")

    return render(request, "prediction.html", {
        "stocks": stock_list,
        "selected_stock": selected_stock,
        "predicted_price": predicted_price,
        "actual_prices": actual_prices,
        "prediction_plot": prediction_plot,
    })
