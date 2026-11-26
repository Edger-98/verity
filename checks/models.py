#from django.db import models

# Create your models here.

from django.db import models
import uuid 
from django.core.validators import MinValueValidator,  MaxValueValidator
from django.conf import settings

class Check(models.Model):


    class Status(models.TextChoices): # enum to allow firldtype to use options 

        PENDING =  'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        DONE = 'done', 'Done'
        FAILED = 'failed', 'Failed'

    class Verdict (models.TextChoices):

        AUTHENTIC = 'authentic', "Authentic"
        AI_GENERATED = "ai_generated", "AI generated"
        UNKNOWN = "unknown", "Unknown"


    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    original_filename = models.CharField(max_length = 255)
    file_hash = models.CharField(db_index=True, editable= False,max_length = 64 )
    status = models.CharField(max_length = 20, choices = Status.choices, default= Status.PENDING )
    verdict  = models.CharField(max_length = 20 , blank=True, choices= Verdict.choices, default = '')
    ai_score = models.FloatField(null= True, validators = [ MinValueValidator(0),  MaxValueValidator(1)])
    c2pa_result = models.JSONField(null = True)
    retry_count = models.PositiveIntegerField(default = 0 )
    error_message = models.TextField(blank = True, default = '')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at=models.DateTimeField(null=True, blank=True)
    completed_at=  models.DateTimeField(null=True, blank=True)
    upload = models.FileField(blank=True, upload_to = 'uploads/')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE , related_name="checks")
