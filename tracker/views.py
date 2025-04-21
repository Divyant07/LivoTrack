from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile, DietPlan, FoodLog
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from .models import UserProfile, ALLERGY_CHOICES
from PIL import Image
from .utils import extract_values_from_image, analyze_liver_stage
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, date
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
import os
import json

def userprofile_register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        age = request.POST.get('age')

        context = {}

        # Password match check
        if password != confirm_password:
            context['error'] = 'Passwords do not match.'
            return render(request, 'tracker/register.html', context)

        # Username uniqueness check
        if User.objects.filter(username=uname).exists():
            context['error'] = 'Username already exists.'
            return render(request, 'tracker/register.html', context)

        # Email format validation
        try:
            validate_email(email)
        except ValidationError:
            context['error'] = 'Invalid email format.'
            return render(request, 'tracker/register.html', context)

        # Email uniqueness check
        if User.objects.filter(email=email).exists():
            context['error'] = 'Email already exists.'
            return render(request, 'tracker/register.html', context)

        # Create user and user profile
        user = User.objects.create_user(username=uname, email=email, password=password)

        profile = UserProfile.objects.create(
            user=user,
            age=age
        )

        return redirect('userprofile_login')

    return render(request, 'tracker/register.html')


def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user_obj = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                return render(request, 'tracker/login.html', {'error': 'Invalid username/email'})

        user = auth.authenticate(username=user_obj.username, password=password)
        if user:
            auth.login(request, user)
            profile = UserProfile.objects.get(user=user)

            # Redirect to onboarding if profile is incomplete
            if not profile.is_profile_complete:
                return redirect('onboarding')

            return redirect('dashboard')  # Your main app page
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid password 😬'})

    return render(request, 'tracker/login.html')

@login_required
def dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    diet_plan = profile.get_matching_diet_plan()
    
    # Use timezone.now() instead of datetime.today()
    today = timezone.now().date()
    today_logs = FoodLog.objects.filter(user_profile=profile, log_time__date=today)

    calorie_limit = 2000
    total_calories = sum(log.calories for log in today_logs)

    if total_calories < calorie_limit * 0.9:
        status = "Off Track (Too Low)"
    elif total_calories > calorie_limit * 1.1:
        status = "Off Track (Too High)"
    else:
        status = "On Track ✅"

    quotes_file_path = os.path.join(os.path.dirname(__file__), './static/tracker/quotes.json')
    with open(quotes_file_path, 'r') as file:
        quotes = json.load(file)

    quote_index = (datetime.now().day + request.user.id) % len(quotes)
    daily_quote = quotes[quote_index]

    if request.method == 'POST':
        food_name = request.POST.get('food_name')
        quantity = request.POST.get('quantity')
        calories = float(request.POST.get('calories'))

        FoodLog.objects.create(
            user_profile=profile,
            food_name=food_name,
            quantity=quantity,
            calories=calories,
            log_time=timezone.now()  # Use timezone-aware datetime here too
        )
        return redirect('dashboard')

    context = {
        'profile': profile,
        'diet_plan': diet_plan,
        'total_calories': total_calories,
        'calorie_limit': calorie_limit,
        'status': status,
        'daily_quote': daily_quote,
        'today_logs': today_logs,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def onboarding(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.diet_preference = request.POST.get('diet_preference')
        profile.allergies = request.POST.get('allergies')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        uploaded_file = request.FILES.get('report_file')

        if uploaded_file:
            if uploaded_file.name.lower().endswith(('jpg', 'jpeg', 'png')):
                profile.report_file = uploaded_file
                profile.save()  # Save first to get file path

                # OCR analysis for image file
                file_path = profile.report_file.path
                image = Image.open(file_path)

                sgpt, sgot = extract_values_from_image(image)
                stage = analyze_liver_stage(sgpt, sgot)
                profile.liver_stage = stage
            else:
                # Optionally show a message if the uploaded file isn’t an image
                return render(request, 'tracker/onboarding.html', {
                    'profile': profile,
                    'error': 'Only JPG/JPEG/PNG image files are supported.'
                })

        profile.is_profile_complete = True
        profile.save()

        return redirect('dashboard')

    return render(request, 'tracker/onboarding.html', {'profile': profile})

def welcome_page(request):
    return render (request, 'tracker/index.html')

@login_required
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.diet_preference = request.POST.get('diet_preference')
        profile.allergies = request.POST.get('allergies')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        profile.save()
        return redirect('dashboard')

    return render(request, 'tracker/edit_profile.html', {
        'profile': profile,
        'allergy_choices': ALLERGY_CHOICES
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep user logged in
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'tracker/change_password.html', {'form': form})

def home(request):
    return render(request, 'tracker/home.html')

@login_required
def report_view(request):
    profile = UserProfile.objects.get(user=request.user)
    today = timezone.now().date()
    
    # Check if we need to reset (new day)
    last_visit_date = request.session.get('last_visit_date')
    is_new_day = str(last_visit_date) != str(today)
    
    if is_new_day:
        # Clear today's data if it's a new day
        FoodLog.objects.filter(
            user_profile=profile,
            log_time__date=today
        ).delete()
        
    # Update last visit date
    request.session['last_visit_date'] = str(today)
    
    # Get today's food logs
    food_logs = FoodLog.objects.filter(
        user_profile=profile, 
        log_time__date=today
    ).order_by('-log_time')
    
    # Calculate age
    age = profile.age if profile.age else 30  # Default to 30 if age not set

    # Calculate BMI and personalized calorie limit
    if profile.height and profile.weight:
        height_m = profile.height / 100  # convert cm to meters
        bmi = profile.weight / (height_m ** 2)
        
        # Base calorie needs calculation (Mifflin-St Jeor Equation)
        bmr = (10 * profile.weight) + (6.25 * profile.height) - (5 * age) - 161
        
        # Activity level estimation based on liver stage
        activity_multiplier = 1.2  # default sedentary
        
        if profile.liver_stage:
            if 'cirrhosis' in profile.liver_stage.lower():
                activity_multiplier = 1.2  # sedentary
            elif 'fibrosis' in profile.liver_stage.lower():
                activity_multiplier = 1.375  # lightly active
            else:
                activity_multiplier = 1.55  # moderately active
        
        # Calculate daily calorie needs
        calorie_limit = round(bmr * activity_multiplier)
        
        # Adjust based on BMI if available
        if bmi > 25:  # overweight
            calorie_limit = max(calorie_limit - 250, 1200)  # ensure minimum 1200 kcal
        elif bmi < 18.5:  # underweight
            calorie_limit += 250
        
    else:
        # Fallback to standard calorie limit if height/weight not set
        calorie_limit = 2000
        bmi = None

    total_calories = sum(log.calories for log in food_logs)
    
    # Calculate status with personalized thresholds
    if total_calories == 0:
        status = "No Data"
        status_class = "info"
    elif total_calories < calorie_limit * 0.9:
        status = "Below Target ⬇️"
        status_class = "warning"
    elif total_calories > calorie_limit * 1.1:
        status = "Above Target ⬆️"
        status_class = "danger"
    else:
        status = "On Target ✅"
        status_class = "success"

    # Prepare chart data
    food_data = {
        'labels': [log.food_name for log in food_logs],
        'calories': [log.calories for log in food_logs],
        'quantities': [log.quantity for log in food_logs]
    }

    # Get matching diet plan if available
    diet_plan = profile.get_matching_diet_plan()

    context = {
        'date': today.strftime('%B %d, %Y'),
        'food_logs': food_logs,
        'total_calories': total_calories,
        'calorie_limit': calorie_limit,
        'status': status,
        'status_class': status_class,
        'food_data': json.dumps(food_data),
        'bmi': round(bmi, 1) if bmi else None,
        'calorie_percentage': round((total_calories / calorie_limit) * 100) if calorie_limit and total_calories else 0,
        'diet_plan': diet_plan,
        'liver_stage': profile.liver_stage,
        'is_new_day': is_new_day,
    }
    return render(request, 'tracker/report.html', context)

@login_required
@require_POST
def reset_daily_data(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        today = timezone.now().date()
        
        # Delete today's food logs
        deleted_count, _ = FoodLog.objects.filter(
            user_profile=profile,
            log_time__date=today
        ).delete()
        
        # Clear the session flag so new day message shows again
        if 'last_visit_date' in request.session:
            del request.session['last_visit_date']
        
        return JsonResponse({
            'success': True,
            'message': f'Reset {deleted_count} food logs for today',
            'is_new_day': True
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
    
@login_required
@require_POST
def check_daily_reset(request):
    """Endpoint for AJAX check if daily reset is needed"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        today = timezone.now().date()
        last_visit_date = request.session.get('last_visit_date')
        is_new_day = str(last_visit_date) != str(today)
        
        return JsonResponse({
            'needs_reset': is_new_day,
            'current_date': str(today)
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)
    