from django.contrib import admin

# Register your models here.
from foodlinebot.models import *

class User_Info_Admin(admin.ModelAdmin):
    list_display = ('uid','name','pic_url','mtext','mdt','state','win','lose')
class Score_Info_Admin(admin.ModelAdmin):
    list_display = ('name','win','lose')
admin.site.register(User_Info,User_Info_Admin)
admin.site.register(Score_Info,Score_Info_Admin)