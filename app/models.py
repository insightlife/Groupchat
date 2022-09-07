from django.db import models

class chat(models.Model):
    content = models.CharField(max_length=255)
    group = models.CharField(max_length=50)
    person = models.CharField(max_length=200)
    timestamp =models.DateTimeField(auto_now=True)
    
class group(models.Model):
    name= models.CharField(max_length=255)  
    def __str__(self):
        return self.name

class Feedback(models.Model):
    Name = models.CharField(max_length=30,default="")
    Email = models.CharField(max_length=50,default="")
    Query = models.CharField(max_length=500,default="")
    made_on = models.DateTimeField(auto_now_add=True)


