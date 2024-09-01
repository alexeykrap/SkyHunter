from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


# Create your models here.


class Matrix(models.Model):
    class Meta:
        verbose_name_plural = 'Матрицы камеры'
        verbose_name = 'Матрица камеры'
        unique_together = ['w_matrix', 'h_matrix']
    w_matrix = models.IntegerField(validators=[MinValueValidator(240)], default=800,
                                   verbose_name='Ширина матрицы')
    h_matrix = models.IntegerField(validators=[MinValueValidator(240)], default=600,
                                   verbose_name='Высота матрицы')

class Camera(models.Model):
    class Meta:
        verbose_name_plural = 'Камеры'
        verbose_name = 'Камера'
        unique_together = []
    manufacturer = models.CharField(max_length=30, verbose_name='Производитель')
    model = models.CharField(max_length=30, verbose_name='Модель')
    matrix = models.ForeignKey(Matrix, related_name='matrix', blank=False, null=True, verbose_name='Матрица',
                               on_delete=models.SET_NULL)


class Equipment(models.Model):
    class Meta:
        verbose_name_plural = 'Оборудование'
        verbose_name = 'Оборудование'
    name = models.CharField(max_length=30, unique=True, verbose_name='Псевдоним')
    manufacturer = models.CharField(max_length=30, verbose_name='Производитель')
    model = models.CharField(max_length=30, verbose_name='Модель')
    note = models.TextField(default='Описание оборудования', blank=False, null=False, verbose_name='Описание')


class Drone(models.Model):
    class Meta:
        verbose_name_plural = 'Дроны'
        verbose_name = 'Дрон'
        unique_together = []

    A = 'A'
    M = 'M'
    D = 'D'
    STATUS_CHOICES = [
        (A, 'airsim'),
        (M, 'mavlink'),
        (D, 'dji')
    ]

    name = models.CharField(max_length=30, unique=True, verbose_name='Псевдоним')
    manufacturer = models.CharField(max_length=30, verbose_name='Производитель')
    model = models.CharField(max_length=30, verbose_name='Модель')
    n_rotors = models.IntegerField(validators=[MinValueValidator(1)], default=4,
                                         verbose_name='Количество моторов')
    api_type = models.CharField(max_length=1, choices=STATUS_CHOICES, default=A, verbose_name='Тип API-интерфейса')
    camera = models.ForeignKey(Camera, related_name='camera', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Камера(ы)')
    equipment = models.ManyToManyField(Equipment, related_name='equipment', blank=True, verbose_name='Оборудование')

    def __str__(self):
        api = 'airsim'
        if self.api_type == 'M':
            api = 'mavlink'
        elif self.api_type == 'D':
            api = 'dji'
        return f'{self.name}, API: {api}'

    def get_url(self):
        return reverse('drone-details', args=[self.id])



