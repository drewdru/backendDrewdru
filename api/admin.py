from django.contrib import admin
from api.models import TaskModel, UserModel, PostModel
# Register your models here.

@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
  	pass

@admin.register(UserModel)
class TaskAdmin(admin.ModelAdmin):
  	pass

@admin.register(PostModel)
class TaskAdmin(admin.ModelAdmin):
  	pass
