from django.db import models

#creating models for admin
# class Admin(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=128)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.username

#         class Meta:
#         db_table = 'cafeteria_admin'