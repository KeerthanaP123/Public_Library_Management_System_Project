# from operator import mod
from django.db import models


# Create your models here.


class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=60)
    type = models.CharField(max_length=60)
    uid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'login'

   
class register(models.Model):
    id = models.IntegerField(db_column='Id', blank=True, null=True)  # Field name made lowercase.
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.CharField(max_length=40,unique=True,primary_key=True)
    contact=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    pincode=models.CharField(max_length=6)
    password=models.CharField(max_length=15)
    confirmpassword=models.CharField(max_length=15,default='True')
    status=models.CharField(max_length=15,default=True)

    class Meta:
        # managed = False
        db_table = 'register_hm'
