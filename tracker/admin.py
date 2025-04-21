from django.contrib import admin
from .models import UserProfile, FoodLog, DietPlan

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'diet_preference', 'allergies', 'liver_stage', 'is_profile_complete')

@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'food_name', 'quantity', 'calories', 'log_time')

@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'liver_stage', 'diet_preference', 'allergy_to_avoid', 'assigned_on')
    list_filter = ('liver_stage', 'diet_preference', 'allergy_to_avoid')
