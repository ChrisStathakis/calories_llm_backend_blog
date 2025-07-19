from typing import Optional, Dict

class BMRCalculator:
    """
    Calculate BMR using various formulas
    """

    @staticmethod
    def mifflin_st_jeor(weight: float, height: float, age: int, gender: str) -> float:
        """
        Mifflin-St Jeor Equation (most accurate for most people)
        Men: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) + 5
        Women: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) - 161
        """
        bmr = 10 * weight + 6.25 * height - 5 * age
        if gender.upper() == 'M':
            bmr += 5
        else:
            bmr -= 161
        return bmr

    @staticmethod
    def harris_benedict(weight: float, height: float, age: int, gender: str) -> float:
        """
        Harris-Benedict Equation (original formula)
        Men: BMR = 88.362 + (13.397 × weight) + (4.799 × height) - (5.677 × age)
        Women: BMR = 447.593 + (9.247 × weight) + (3.098 × height) - (4.330 × age)
        """
        if gender.upper() == 'M':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        return bmr

    @staticmethod
    def katch_mcardle(weight: float, body_fat_percentage: float) -> float:
        """
        Katch-McArdle Formula (requires body fat percentage)
        BMR = 370 + (21.6 × lean body mass in kg)
        """
        lean_body_mass = weight * (1 - body_fat_percentage / 100)
        bmr = 370 + (21.6 * lean_body_mass)
        return bmr

    @staticmethod
    def cunningham(weight: float, body_fat_percentage: float) -> float:
        """
        Cunningham Formula (for athletes/very active people)
        BMR = 500 + (22 × lean body mass in kg)
        """
        lean_body_mass = weight * (1 - body_fat_percentage / 100)
        bmr = 500 + (22 * lean_body_mass)
        return bmr

    @staticmethod
    def calculate_tdee(bmr: float, activity_level: float) -> float:
        """
        Calculate Total Daily Energy Expenditure
        TDEE = BMR × Activity Level
        """
        return bmr * activity_level

    @classmethod
    def calculate_all_bmr(cls, weight: float, height: float, age: int,
                          gender: str, activity_level: float = 1.2,
                          body_fat_percentage: Optional[float] = None) -> Dict:
        """
        Calculate BMR using all applicable formulas
        """
        results = {}

        # Mifflin-St Jeor (most recommended)
        mifflin_bmr = cls.mifflin_st_jeor(weight, height, age, gender)
        results['mifflin'] = {
            'bmr': mifflin_bmr,
            'tdee': cls.calculate_tdee(mifflin_bmr, activity_level),
            'formula_name': 'Mifflin-St Jeor',
            'recommended': True
        }

        # Harris-Benedict
        harris_bmr = cls.harris_benedict(weight, height, age, gender)
        results['harris'] = {
            'bmr': harris_bmr,
            'tdee': cls.calculate_tdee(harris_bmr, activity_level),
            'formula_name': 'Harris-Benedict',
            'recommended': False
        }

        # Katch-McArdle (if body fat percentage provided)
        if body_fat_percentage is not None:
            katch_bmr = cls.katch_mcardle(weight, body_fat_percentage)
            results['katch'] = {
                'bmr': katch_bmr,
                'tdee': cls.calculate_tdee(katch_bmr, activity_level),
                'formula_name': 'Katch-McArdle',
                'recommended': False
            }

            # Cunningham (for athletes)
            cunningham_bmr = cls.cunningham(weight, body_fat_percentage)
            results['cunningham'] = {
                'bmr': cunningham_bmr,
                'tdee': cls.calculate_tdee(cunningham_bmr, activity_level),
                'formula_name': 'Cunningham',
                'recommended': False
            }

        return results