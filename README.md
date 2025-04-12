# finwise

FinWise is a Django-based web application designed to assist small-scale workers and users with limited financial literacy. The platform combines financial tools, AI support, and accessibility features to offer inclusive, intelligent, and user-friendly financial assistance.
1.. AI Assistant (Kannada)
Voice/Chat-based Assistant integrated using AI .Supports FAQs and guidance related to personal finance in Kannada.Helps users understand concepts like saving, investments, loans, and financial planning.
2. Wealth Management 
Visualizes Budget vs Expenses through interactive bar charts (using Chart.js).Users can input monthly budgets and expenses, and view them in graphical form.Offers insights into overspending or underspending trends.
3.Step-by-Step Guide to Open a Bank Account
Simple, readable guide that walks users through:Required documentsDifferent types of accounts (e.g., savings/current)Online/offline application processSafety tips and do's & don’ts
4.  Finance Assistant
Accepts user inputs (income, expenses, dependents, etc.) and gives personalized financial suggestions.Recommendations on budgeting, emergency funds, and investment planning.
5. Finance Education
Educational content in simple language covering:Budgeting


Folder and File Structure

Here is how the files and folders should be organized in the project:

1. Main Project Folder (hackathon/)

This is the core Django project folder. It should contain:

_init_.py

settings.py

urls.py

asgi.py

wsgi.py



2. App Folder (accounts/)

This is your Django app folder for account-related and financial features. It should contain:

_init_.py

admin.py – for registering models in the Django admin panel

apps.py – for app configuration

forms.py – for Django forms

models.py – for database models

tests.py – for writing tests

urls.py – for app-specific URL routes

views.py – for writing backend logic and view functions




3. Templates Folder (accounts/templates/accounts/)

Inside your app, create the following structure for templates:

home.html

login.html

signup.html

dashboard.html

financeeducation.html

create_account_steps.html


For financial assistant views, create a subfolder:

accounts/templates/accounts/finance_assistant_view/investment_suggestor.html




4. Media Folder (media/)

This folder is just for storing the files like when you run the AI assisant the voice will be stored here


5. Database File (db.sqlite3)

This file is automatically created after running migrations. It stores all your data.



6. Virtual Environment Folder (venv/)

This is the Python virtual environment where all required packages are installed. This folder should not be pushed to GitHub. Make sure to add it to your .gitignore.



7. Manage File (manage.py)

This is the main script used to run Django commands like runserver, makemigrations, etc.



8. Pycache Folder (_pycache_/)

This is an automatically generated folder that stores compiled Python files. You don’t need to touch or push this folder to GitHub.




