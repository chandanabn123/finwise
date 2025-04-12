from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import FinancialGoal
import os, json
from django.views.decorators.http import require_POST


# Load environment variables

# Sign-up
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('dashboard')
# Home
def home_view(request):
    return render(request, 'accounts/home.html')

# Dashboard
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')



# Finance Assistant View
@login_required(login_url='login')
def finance_assistant_view(request):
    error = None
    if request.method == 'POST':
        try:
            age = int(request.POST.get('age', 0))
            income = int(request.POST.get('income', 0))
            expenses = int(request.POST.get('expenses', 0))
            risk = request.POST.get('risk_appetite', 'medium')
            goal = request.POST.get('goal', '')

            if income <= 0 or expenses < 0 or age <= 0:
                raise ValueError("Please fill all fields correctly.")

            savings = income - expenses
            amount_to_invest = savings * 0.3 if savings > 0 else 0

            beginner_plans = [
                "1. Start a Recurring Deposit (RD)",
                "2. Invest small amounts in SIPs (Mutual Funds)",
                "3. Open a Sukanya Samriddhi or PPF Account"
            ]

            tax_saving_tips = [
                "Invest in ELSS Mutual Funds under Section 80C",
                "Buy Health Insurance (Deduction under 80D)",
                "Use NPS (National Pension Scheme) for extra 50K deduction"
            ]

            if age < 20:
                plans = beginner_plans
                recommended_bank = "Post Office or Paytm Money"
            else:
                if risk == 'low':
                    plans = ["PPF", "Fixed Deposits", "Post Office Schemes"]
                    recommended_bank = "SBI, Post Office"
                elif risk == 'medium':
                    plans = ["Balanced Mutual Funds", "Gold ETFs", "Life Insurance"]
                    recommended_bank = "HDFC, Axis Mutual Fund"
                else:
                    plans = ["Equity Funds", "SIP in Small-Caps", "Direct Stocks"]
                    recommended_bank = "Zerodha, Groww"

            graph_labels = ['Low Risk', 'Medium Risk', 'High Risk']
            graph_values = [2, 5, 9] if age < 20 else [3, 6, 9]
            monthly_saving_projection = [round(savings * (1 + 0.02 * i)) for i in range(6)] if savings > 0 else [0] * 6

            user_goals = FinancialGoal.objects.filter(user=request.user)

            suggestions = {
                'plans': plans,
                'bank': recommended_bank,
                'income': income,
                'expenses': expenses,
                'savings': savings,
                'amount': round(amount_to_invest),
                'graph_labels_json': json.dumps(graph_labels),
                'graph_values_json': json.dumps(graph_values),
                'monthly_projection_json': json.dumps(monthly_saving_projection),
                'ai_response': None,
                'goals': user_goals,
                'tax_tips': tax_saving_tips
            }

            return render(request, 'finance_assistant_view/investment_suggestor.html', {
                'suggestions': suggestions,
                'error': None
            })

        except Exception as e:
            error = str(e)

    # For GET or in case of error
    suggestions = {
        'plans': [],
        'bank': '',
        'income': 0,
        'expenses': 0,
        'savings': 0,
        'amount': 0,
        'graph_labels_json': json.dumps(['Low Risk', 'Medium Risk', 'High Risk']),
        'graph_values_json': json.dumps([0, 0, 0]),
        'monthly_projection_json': json.dumps([0] * 6),
        'ai_response': None,
        'goals': FinancialGoal.objects.filter(user=request.user),
        'tax_tips': []
    }

    return render(request, 'finance_assistant_view/investment_suggestor.html', {
        'suggestions': suggestions,
        'error': error
    })


from django.shortcuts import render
from django.http import JsonResponse
from gtts import gTTS
import os
import uuid
from difflib import get_close_matches  # 👈 NEW

def AIAssistant(request):
    return render(request, 'accounts/AIAssistant.html')


    # FAQ dictionary
FAQS = {
    "ನಾನು ತಿಂಗಳಿಗೆ ಎಷ್ಟು ಉಳಿಸಬೇಕು?": "ಸಾಧಾರಣವಾಗಿ ನಿಮ್ಮ ಆದಾಯದ ಕನಿಷ್ಠ 20% ಉಳಿಸಲು ಪ್ರಯತ್ನಿಸಿ.",
    "ನಾನು ಸಪ್ತಾಹಿಕ ಸಂಬಳ ಹೊಂದಿದ್ದರೆ ಹೇಗೆ ಯೋಜನೆ ಮಾಡೋದು?": "ನೀವು ದಿನನಿತ್ಯದ ಖರ್ಚಿಗೆ ಒಂದು ಭಾಗ ಮೀಸಲಿಡಿ ಮತ್ತು ಉಳಿದದನ್ನು ಉಳಿತಾಯ ಮಾಡಿ.",
    "ನಾನು ಯಾವ ಖರ್ಚುಗಳನ್ನು ಕಡಿಮೆ ಮಾಡಬೇಕು?": "ಅಗತ್ಯವಿಲ್ಲದ ಅಂಚೆಗಳಿಗೆ ಹಾಗೂ ಅತಿ ಹೆಚ್ಚು ಖರ್ಚು ಆಗುವ ವಿಷಯಗಳಿಗೆ ಕತ್ತರಿಸಿ.",
    "EMI ಅಂದ್ರೆ ಏನು? ಅದರಲ್ಲಿ ಸಿಕ್ಕಾಪಟ್ಟೆ ಕಷ್ಟವೇನು?": "EMI (ಇಎಂಐ) ಅಂದ್ರೆ ತಿಂಗಳಿಗೆ ಪಾವತಿಸಬೇಕಾದ ಕಂತು. ಸರಿಯಾಗಿ ಪಾವತಿಸದಿದ್ದರೆ ಬಡ್ಡಿದರ ಹೆಚ್ಚಾಗುತ್ತದೆ ಮತ್ತು ಸಾಲದ ಮೊತ್ತ ಹೆಚ್ಚಾಗಬಹುದು.",
    "ಬಲವಾದ ಉಳಿತಾಯದ ಗುರಿ ಹೇಗೆ ಇಡುವುದು?": "ನಿಮ್ಮ ಗುರಿ ಸ್ಪಷ್ಟವಾಗಿರಲಿ ಮತ್ತು ಅದರ ವೇಳಾಪಟ್ಟಿ ಮಾಡಿ.",
    
    # 👇 New FAQs
    "ಬ್ಯಾಂಕ್ ಖಾತೆ ಹೇಗೆ ತೆರೆಯುವುದು?": "ಅದಕ್ಕಾಗಿ ಗುರುತಿನ ಕಾರ್ಡ್ (ಆಧಾರ್, ಪ್ಯಾನ್), ಫೋಟೋ ಮತ್ತು ವಿಳಾಸ ಪುರಾವೆ ಬೇಕಾಗುತ್ತದೆ. ನೀವು ಹತ್ತಿರದ ಬ್ಯಾಂಕ್‌ಗೆ ಹೋಗಿ ಫಾರ್ಮ್ ಭರ್ತಿ ಮಾಡಬಹುದು.",
    "ಸೇವಿಂಗ್ ಖಾತೆ ಅಂದ್ರೆ ಏನು?": "ಸೇವಿಂಗ್ ಖಾತೆ ಒಂದು ಸಾಮಾನ್ಯ ಬ್ಯಾಂಕ್ ಖಾತೆ ಆಗಿದ್ದು, ಇದರಲ್ಲಿ ನೀವು ಹಣ ಉಳಿಸಬಹುದು ಮತ್ತು ಬಡ್ಡಿ ಕೂಡ ಪಡೆಯಬಹುದು.",
    "ಬಡ್ಡಿದರ ಅಂದ್ರೆ ಏನು?": "ಬಡ್ಡಿದರ ಅಂದ್ರೆ ನಿಮ್ಮ ಉಳಿತಾಯದ ಮೇಲೆ ಬ್ಯಾಂಕ್ ನೀಡುವ ಶೇಕಡಾವಾರು ಮೊತ್ತ.",
    "ಡೆಬಿಟ್ ಕಾರ್ಡ್ ಮತ್ತು ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ ವ್ಯತ್ಯಾಸವೇನು?": "ಡೆಬಿಟ್ ಕಾರ್ಡ್ ನಿಮ್ಮ ಖಾತೆಯಲ್ಲಿ ಇರುವ ಹಣವನ್ನು ಬಳಸುತ್ತದೆ. ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್‌ನಲ್ಲಿ ಬ್ಯಾಂಕ್ ನೀಡಿದ ಕ್ರೆಡಿಟ್ ಅನ್ನು ನೀವು ಬಳಸಬಹುದು.",
    "ನಾನು ಎಷ್ಟರವರೆಗೆ ಉಚಿತ ಬ್ಯಾಂಕ್ ಖಾತೆ ಇರಿಸಿಕೊಳ್ಳಬಹುದು?": "ಬಹುತೆಕ ಬ್ಯಾಂಕ್‌ಗಳು ಮೌಲ್ಯಮಾಪನ ಶೂಲ್ಕವಿಲ್ಲದೆ ಮೂಲ ಸೇವೆಗಳಿಗಾಗಿ ಖಾತೆ ನೀಡುತ್ತವೆ. ನಿಯಮಗಳು ಬ್ಯಾಂಕ್ ಪ್ರಕಾರ ಬದಲಾಗಬಹುದು.",
}

def steps_to_create_account(request):
    return render(request, 'accounts/create_account_steps.html')

def financeeducation(request):
    return render(request, 'accounts/financeeducation.html')

def chatbot_view(request):
    query = request.GET.get('query', '').strip()
    lang = request.GET.get('lang', 'kn')

    # 🧠 Use fuzzy matching to find closest FAQ
    matches = get_close_matches(query, FAQS.keys(), n=1, cutoff=0.5)

    if matches:
        response = FAQS[matches[0]]
    else:
        response = "ಕ್ಷಮಿಸಿ, ನಾನು ಈ ಪ್ರಶ್ನೆಗೆ ಉತ್ತರ ನೀಡಲು ಸಾಧ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ಇನ್ನೊಂದು ರೀತಿಯಲ್ಲಿ ಕೇಳಿ."

    # 🎵 Generate audio
    os.makedirs("media", exist_ok=True)
    filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join("media", filename)
    tts = gTTS(response, lang=lang)
    tts.save(audio_path)

    return JsonResponse({
        'response': response,
        'audio': f'/media/{filename}',
    })

# views.py
from django.shortcuts import render, redirect
from .forms import BudgetEntryForm
from .models import BudgetEntry
import json

def budget_tracker(request):
    if request.method == 'POST':
        form = BudgetEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_tracker')
    else:
        form = BudgetEntryForm()

    entries = BudgetEntry.objects.all()
    chart_data = [
        {
            'month': entry.month,
            'budget': entry.budget,
            'expenses': entry.expenses
        }
        for entry in entries
    ]

    context = {
        'form': form,
        'chart_data': json.dumps(chart_data)
    }
    return render(request, 'accounts/budget_tracker.html', context)
