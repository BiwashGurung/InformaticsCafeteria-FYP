from django.db import models
from cafeteria.models import FoodItem

class EventPopup(models.Model):
    event_id = models.AutoField(primary_key=True) 
    event_title = models.CharField(max_length=255) 
     # To store Image in /media/popups/ 
    image = models.ImageField(upload_to='popups/') 
    start_date = models.DateTimeField()  
    end_date = models.DateTimeField()  

    # To display event_title in admin panel
    def __str__(self):
        return self.event_title
    #Creating a Custom table name in MYSQL
    class Meta:
        db_table = 'event_popups'  
