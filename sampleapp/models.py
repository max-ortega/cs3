from django.db import models

# Create your models here.
class Employee(models.Model):  
    name = models.CharField(max_length=254)  
    email = models.CharField(max_length=254)  
    contact = models.CharField(max_length=254) 
   
    class Meta:  
        db_table = "tblemployee"
