from django.db import models

# Create your models here.
class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')         #user_id
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    pic_url = models.CharField(max_length=255,null=False)               #大頭貼網址
    mtext = models.CharField(max_length=255,blank=True,null=False)      #文字訊息紀錄
    mdt = models.DateTimeField(auto_now=True)                           #物件儲存的日期時間
    state = models.CharField(max_length=255,blank=True,null=False)      #紀錄state
    win = models.IntegerField()
    lose = models.IntegerField()
    def __str__(self):
        return self.uid

class Score_Info(models.Model):
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    win = models.IntegerField()
    lose = models.IntegerField()
    def __str__(self):
        return self.name
