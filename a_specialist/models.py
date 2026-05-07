from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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
    image = models.ImageField(upload_to="avatar/", null=True, blank=True)

    class Meta:
            # ordering = ['-created']
            db_table = 'a_specialist_specialist'
            verbose_name = 'Специалист'
            verbose_name_plural = 'Специалисты'
            
    def __str__(self):
         return f'{self.role}: {self.f_name} {self.l_name}'