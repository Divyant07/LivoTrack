# Generated by Django 5.2 on 2025-04-14 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_remove_userprofile_sgot_remove_userprofile_sgpt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='allergies',
            field=models.CharField(blank=True, choices=[('Dairy', 'Dairy'), ('Gluten', 'Gluten'), ('Nuts', 'Nuts'), ('Peanuts', 'Peanuts'), ('Soy', 'Soy'), ('Eggs', 'Eggs'), ('Shellfish', 'Shellfish'), ('Fish', 'Fish'), ('Sesame', 'Sesame'), ('Wheat', 'Wheat')], max_length=100),
        ),
    ]
