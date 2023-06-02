# Create your models here.
from django.contrib.auth.models import User
from django.db import models



class Booklet(models.Model):
    title = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='booklets')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
