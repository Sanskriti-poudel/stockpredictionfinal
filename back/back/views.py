import os
import json
import joblib
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from tensorflow import keras

def home(request):
    return render(request, "home.html")

def user_login(request):
    return render(request, "login.html")

def chart(request):
    return render(request, "chart.html")

def portfolio(request):
    return render(request, "portfolio.html")

def announcement(request):
    return render(request, "announcement.html")

def payment(request):
    return render(request, "payment.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

def dashboard(request):
    return render(request, "dashboard.html")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def prediction(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

    if selected_stock:
        print(f"Selected stock: {selected_stock}")
        try:
            data_path = os.path.join(data_dir, f"{selected_stock}.json")
            with open(data_path) as f:
                historical_data = json.load(f)

            prices = [entry["LTP"] for entry in historical_data if "LTP" in entry]
            actual_prices = prices
            print(f"Found {len(prices)} prices in historical data.")

            predicted_price = predicted_ltp_data.get(selected_stock.lower())
            print(f"Predicted price from JSON: {predicted_price}")

        except Exception as e:
            print(f"Error processing stock {selected_stock}: {e}")

    return render(request, "prediction.html", {
        "stocks": stock_list,
        "selected_stock": selected_stock,
        "predicted_price": predicted_price,
        "actual_prices": actual_prices,
    })
