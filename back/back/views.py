# stockprediction/views.py

import os
import pandas as pd
import numpy as np
import joblib
from tensorflow import keras
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# cache to avoid repeated model reloads
loaded_models = {}

# === HTML PAGE VIEWS ===

def home(request):
    return render(request, 'home.html')

def user_login(request):
    # if request.method == "POST":
    #     password = request.POST.get("password")
    #     username = request.POST.get("username")`
    # `
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def chart(request):
    return render(request, 'chart.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def prediction(request):
    return render(request, 'prediction.html')

def announcement(request):
    return render(request, 'announcement.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def payment(request):
    return render(request, 'payment.html')


# === API VIEWS ===

def predict_stock(request):
    symbol = request.GET.get("symbol")
    if not symbol:
        return JsonResponse({"error": "Missing symbol"}, status=400)

    # load model if not already cached
    if symbol not in loaded_models:
        try:
            model_path = os.path.join(
                "stockprediction", "allsavedmodels", "gru_fundamental", f"{symbol}_GRU.keras"
            )
            x_scaler_path = os.path.join(
                "stockprediction", "allsavedmodels", "gru_fundamental", f"{symbol}_scaler.save"
            )
            y_scaler_path = os.path.join(
                "stockprediction", "allsavedmodels", "gru_fundamental", f"{symbol}_y_scaler.save"
            )
            model = keras.models.load_model(model_path)
            x_scaler = joblib.load(x_scaler_path)
            y_scaler = joblib.load(y_scaler_path)
            loaded_models[symbol] = (model, x_scaler, y_scaler)
        except Exception as e:
            return JsonResponse({"error": f"Failed to load model for {symbol}: {str(e)}"}, status=500)

    model, x_scaler, y_scaler = loaded_models[symbol]

    # load historical data
    file_path = os.path.join(
        "stockprediction", "data", "historical", f"{symbol.lower()}.xlsx"
    )
    if not os.path.exists(file_path):
        return JsonResponse({"error": f"No historical data for {symbol}"}, status=404)

    try:
        df = pd.read_excel(file_path)
        df = df.head(30)
        features = df[["LTP", "High", "Low", "Open", "Qty.", "Turnover"]].values
        latest_ltp = float(df.iloc[0]["LTP"])
        features_scaled = x_scaler.transform(features.reshape(-1, features.shape[1])).reshape(1, 30, features.shape[1])
        y_pred_scaled = model.predict(features_scaled)
        y_pred = y_scaler.inverse_transform(y_pred_scaled)
    except Exception as e:
        return JsonResponse({"error": f"Error processing prediction: {str(e)}"}, status=500)

    return JsonResponse({
        "symbol": symbol,
        "latest_ltp": latest_ltp,
        "predicted_price": float(y_pred[0][0])
    })


def stock_list_api(request):
    model_path = "stockprediction/allsavedmodels/gru_fundamental/"
    stocks = []
    try:
        model_files = set(
            f.replace("_GRU.keras", "") for f in os.listdir(model_path) if f.endswith("_GRU.keras")
        )
        stocks = sorted(list(model_files))
    except Exception as e:
        return JsonResponse({"error": f"Error listing stocks: {str(e)}"}, status=500)

    return JsonResponse(stocks, safe=False)
