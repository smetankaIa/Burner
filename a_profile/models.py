from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import localdate

import uuid

# from datetime import timedelta


# Create your models here.
class Profile(models.Model):
    class Male(models.TextChoices):
        MAN = "Мужской", "Мужской"
        WOMAN = (
            "Женский",
            "Женский",
        )
        NONE = "Не указан", "Не указан"

    class Goal(models.TextChoices):
        LOSS = "Сброс", "Сброс"
        MAINTANE = (
            "Поддержание",
            "Поддержание",
        )
        ADD = "Набор", "Набор"

    class Activity(models.IntegerChoices):
        SEAT = 1, "Отсутствие тренировок"
        LIGHT = 2, "1–3 тренировки в неделю"
        MID = 3, "3–5 тренировок в неделю"
        HIGH = 4, "6–7 тренировок в неделю"
        OVERHIGH = 5, "Профессиональный спорт"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    f_name = models.CharField(max_length=20, blank=True, default="Имя")
    l_name = models.CharField(max_length=20, blank=True, default="Фамилия")
    email = models.EmailField( blank=True)
    male = models.CharField(max_length=20, choices=Male.choices, default=Male.NONE)
    goal = models.CharField(max_length=20, choices=Goal.choices, default=Goal.MAINTANE)
    activity = models.IntegerField(choices=Activity.choices, default=Activity.LIGHT)
    plusstatus = models.BooleanField(default=False)
    height = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    weight = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    dete_birth = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        if not self.dete_birth:
            return 0

        today = datetime.date.today()

        years = today.year - self.dete_birth.year

        if (today.month, today.day) < (self.dete_birth.month, self.dete_birth.day):
            years -= 1

        return years

    @property
    def target_calories(self):
        try:
            weight = float(self.weight)
            height = float(self.height)
        except (TypeError, ValueError):
            return 2000

        if not weight or not height:
            return 2000

        # BMR
        if self.male == "WOMAN":
            bmr = (10 * weight) + (6.25 * height) - (5 * self.age) - 161
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * self.age) + 5

        # Activity
        activity_map = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}
        tdee = bmr * activity_map.get(self.activity, 1.2)

        # Goal
        goal = (self.goal or "").lower()

        if goal == "сброс":
            tdee *= 0.8
        elif goal == "набор":
            tdee *= 1.1

        return int(tdee)

    @property
    def target_proteins(self):
        # 2 грамма белка на 1 кг веса
        return int(self.weight * 2) if self.weight else 100

    @property
    def target_fats(self):
        # 1 грамм жира на 1 кг веса
        return int(self.weight * 1) if self.weight else 60

    @property
    def target_carbs(self):
        # Углеводы = (Оставшиеся калории от белков и жиров) / 4
        # 1г белка = 4 ккал, 1г жира = 9 ккал, 1г углеводов = 4 ккал
        cals_from_pf = (self.target_proteins * 4) + (self.target_fats * 9)
        remaining = self.target_calories - cals_from_pf
        return int(remaining / 4) if remaining > 0 else 150

    @property
    def today_totals(self):
        # Получаем сегодняшнюю дату
        today = datetime.date.today()

        # Ищем все записи питания для этого профиля за сегодня
        # Используем date_eat__date, так как date_eat это DateTimeField
        meals_today = self.user.nutricion_set.filter(date_meal__date=today)

        # Складываем значения.
        # Так как total_calories и т.д. это @property, мы суммируем их через генератор (sum)
        cals = sum(meal.total_calories for meal in meals_today)
        prot = sum(meal.total_protein for meal in meals_today)
        fat = sum(meal.total_fat for meal in meals_today)
        carbs = sum(meal.total_carbs for meal in meals_today)

        return {
            "cals": round(cals),
            "prot": round(prot),
            "fat": round(fat),
            "carbs": round(carbs),
        }

    @property
    def today_workout(self):
        today = localdate()
        # Ищем тренировку пользователя на сегодняшний день.
        # Если она есть - возвращаем её, если нет - возвращаем None
        return self.user.workouts.filter(date__date=today).first()

    def __str__(self):
        return str(self.user)



class Specialist(models.Model):
    class Role(models.TextChoices):
        DOCTOR = "Врач", "Врач"
        COACH = (
            "Тренер",
            "Тренер",
        )
        ANOTHER = "Другое", "Другое"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="specialist"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.ANOTHER)
    about = models.TextField(max_length=150, default="Специалист")
    f_name = models.CharField(max_length=20, blank=True, default="Имя")
    l_name = models.CharField(max_length=20, blank=True, default="Фамилия")
    number = models.CharField(max_length=11, null=True)
    social_tg = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="avatar/", null=True, blank=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    

    class Meta:
            
            db_table = 'a_profile_specialist'
            verbose_name = 'Специалист'
            verbose_name_plural = 'Специалисты'
            
    def __str__(self):
         return f'{self.role}: {self.f_name} {self.l_name}'