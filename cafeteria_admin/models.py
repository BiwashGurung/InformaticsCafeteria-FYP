from django.db import models
from cafeteria.models import FoodItem
from django.contrib.auth.models import User


# Creating an EventPopup model to store event-related information for the popup
class EventPopup(models.Model):
    event_id = models.AutoField(primary_key=True) 
    event_title = models.CharField(max_length=255) 
    # Field to store the event image in the /media/popups/ directory
    image = models.ImageField(upload_to='popups/') 
    start_date = models.DateTimeField()  
    end_date = models.DateTimeField()  

    # To display event_title in admin panel
    def __str__(self):
        return self.event_title
    #Creating a Custom table name in MYSQL
    class Meta:
        db_table = 'event_popups'  


