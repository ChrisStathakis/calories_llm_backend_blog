import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from profiles.bmr_calculator import BMRCalculator

User = get_user_model()

class Profile(models.Model):
    ACTIVITY_LEVELS = [
        (1.2, 'Sedentary (little/no exercise)'),
        (1.375, 'Lightly active (light exercise/sports 1-3 days/week)'),
        (1.55, 'Moderately active (moderate exercise/sports 3-5 days/week)'),
        (1.725, 'Very active (hard exercise/sports 6-7 days a week)'),
        (1.9, 'Super active (very hard exercise/physical job)'),
    ]

    GENDER_OPTIONS = (
        ("M", "MALE"),
        ("F", "FEMALE")
    )

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="profile")
    height = models.IntegerField(max_length=3)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    activity_lvl = models.FloatField(choices=ACTIVITY_LEVELS, default=1.2)
    year_of_birth = models.DateField()
    calories = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    bmr = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS)

    def save(self, *args, **kwargs):
        if self.id:
            self.age = self.calculate_age()
            self.bmr = BMRCalculator.harris_benedict(
                weight=float(self.weight),
                height=float(self.height),
                age=self.age,
                gender=self.gender
            )
            self.calories = BMRCalculator.calculate_tdee(self.bmr, self.activity_lvl)
        super().save(*args, **kwargs)

    def calculate_age(self):
        """
        Calculate exact age based on current date
        """

        today = datetime.datetime.today()
        age = today.year - self.year_of_birth.year #  int(self.year_of_birth.split("-")[0])

        # Check if birthday hasn't occurred this year
        """
        if (today.month, today.day) < (datetime.datetime.strptime(self.birth, "%Y-%m-%d").date().month,
                                       datetime.datetime.strptime(self.birth, "%Y-%m-%d").date().day):
            age -= 1
        print("age", age)
        """
        return age

class TargetCalories(models.Model):
    OPTIONS_OF_TARGET = (
        ("A", "CALORIES FOCUS"),
        ("B", "PROTEIN FOCUS"),
        ("C", "CALORIES AND PROTEIN FOCUS")
    )
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    target = models.CharField(max_length=1, choices=OPTIONS_OF_TARGET)
    calories = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def show_target(self):
        if self.target == "A":
            return f"Calories: {self.calories} Kcal"
        elif self.target == "B":
            return f"Protein: {self.protein} gr"
        else:
            return f"Calories: {self.calories} Kcal | Protein: {self.protein} gr"