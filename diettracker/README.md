📊 LivoTrack

LivoTrack is a Django-powered diet tracking web app tailored for users with fatty liver conditions.
It analyzes users' medical reports, identifies their liver condition stage, and generates personalized diet plans to help them manage and improve their health.

🥑 What’s Inside

User Onboarding
Users register, log in, and submit personal info along with a PDF/JPG of their fatty acid report.

Smart OCR Analysis
Uses OCR (Optical Character Recognition) to extract SGPT and SGOT values, determining the user's fatty liver stage automatically.

Personalized Diet Plans
Based on the diagnosed stage and user preferences (veg/non-veg, allergies), admins assign tailored diet plans.

Food Intake Logger
Users can log their daily meals with quantity and calorie info.

Daily Motivational Quotes
Pulls a fresh quote daily from a pool of 200+ to keep spirits high.

Dashboard Insights
Displays condition stage, diet plan, daily logs, and motivational quotes in a clean dashboard UI.

🛠️ Tech Stack

Django — Backend framework

SQLite3 — Database

Pytesseract — OCR library for report analysis

HTML5 / CSS3 / Bootstrap — Frontend

ApexCharts (Optional) — For reports & data visualization

📸 Screenshots

Coming soon — stay tuned!

🚀 Getting Started

1️⃣ Clone the repo:
git clone https://github.com/Divyant07/LivoTrack.git
cd LivoTrack

2️⃣ Install dependencies:
pip install -r requirements.txt

3️⃣ Run migrations:
python manage.py migrate

4️⃣ Start the server:
python manage.py runserver
Now hit http://127.0.0.1:8000/ in your browser.

📂 Project Structure

LivoTrack/
├── tracker/               # Main app
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── ...
├── media/                  # Uploaded reports
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

🎯 Features to Build Next

📈 Food Impact Reports

💬 Real-time User Feedback

📱 Mobile Responsive Layout

🔐 Multi-level Admin System

📣 Contribution

Feel free to fork it, raise issues, or open a pull request — good ideas are always welcome here ✨

📧 Contact

Wanna collab or pitch ideas? Hit me up: [divyantm@example.com]