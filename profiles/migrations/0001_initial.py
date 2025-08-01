# Generated by Django 5.2.3 on 2025-07-14 23:51

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField(max_length=3)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('activity_lvl', models.FloatField(choices=[(1.2, 'Sedentary (little/no exercise)'), (1.375, 'Lightly active (light exercise/sports 1-3 days/week)'), (1.55, 'Moderately active (moderate exercise/sports 3-5 days/week)'), (1.725, 'Very active (hard exercise/sports 6-7 days a week)'), (1.9, 'Super active (very hard exercise/physical job)')], default=1.2)),
                ('year_of_birth', models.DateField()),
                ('calories', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('bmr', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(120)])),
                ('gender', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TargetCalories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(choices=[('A', 'CALORIES FOCUS'), ('B', 'PROTEIN FOCUS'), ('C', 'CALORIES AND PROTEIN FOCUS')], max_length=1)),
                ('calories', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('protein', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
    ]
