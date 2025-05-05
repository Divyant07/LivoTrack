from django.db import models
from django.contrib.auth.models import User

ALLERGY_CHOICES = [
        ('Dairy', 'Dairy'),
        ('Nuts', 'Nuts'),
        ('None', 'None'),
    ]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_profile_complete = models.BooleanField(default=False)

    # Health info
    diet_preference = models.CharField(max_length=10, choices=[('veg', 'Veg'), ('nonveg', 'Non-Veg')], blank=True)
    allergies = models.CharField(max_length=100, choices=ALLERGY_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)
    liver_stage = models.CharField(max_length=20, blank=True, null=True)

    def get_matching_diet_plan(self):
        diet_plans = DietPlan.objects.filter(
            liver_stage=self.liver_stage,
            diet_preference=self.diet_preference,
            allergy_to_avoid=self.allergies
        )
        return diet_plans.first()


    def __str__(self):
        return self.user.username


    
class FoodLog(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='food_logs')
    food_name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    calories = models.FloatField()
    log_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.food_name} - {self.user_profile.user.username} ({self.log_time.strftime('%Y-%m-%d')})"

class DietPlan(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    liver_stage = models.CharField(max_length=20, blank=True, null=True)
    diet_preference = models.CharField(max_length=10, choices=[('veg', 'Veg'), ('nonveg', 'Non-Veg')], blank=True)
    allergy_to_avoid = models.CharField(max_length=100, choices=ALLERGY_CHOICES, blank=True)

    breakfast = models.TextField(blank=True)
    lunch = models.TextField(blank=True)
    dinner = models.TextField(blank=True)
    snacks = models.TextField(blank=True)

    assigned_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.liver_stage}, {self.diet_preference})"
