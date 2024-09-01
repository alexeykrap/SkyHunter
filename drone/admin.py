from django.contrib import admin
from .models import Matrix, Camera, Equipment, Drone

# Register your models here.
@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    ordering = ['w_matrix', 'h_matrix']


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    ordering = ['manufacturer']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    ordering = ['name']


@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    ordering = ['name']