
from django.db import models

from django.contrib.auth.models import User



class Topic(models.Model):
    """用户学习主题"""
   
    text = models.CharField(max_length=200) 
    """记录文本不超过200"""
    
    date_added = models.DateTimeField(auto_now_add=True) 
    """记录保存的时间"""

    owner = models.ForeignKey(User)

    def __str__(self):
        """返回模型的字符表示"""
        return self.text



class Entry(models.Model):
    """学到打有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text[:50] + "..."






# Create your models here.
