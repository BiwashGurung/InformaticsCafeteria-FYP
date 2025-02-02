from django.db import models
from django.contrib.auth.models import User

#Creating a profile model to store additional information about the user in MySQL database
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=50,default='informatics.cafetera@icp.edu.np')
    

    #String representation of the model 
    def __str__(self):
        return self.user.username
    #Custom table name
    class Meta:
        db_table = 'cafeteria_users'    