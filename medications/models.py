from django.db import models

class Drug(models.Model):
    edi_code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    image_url = models.URLField(null=True, blank=True)
    effect_summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class MedicationLog(models.Model):
    user_id = models.CharField(max_length=50) 
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    date_to_take = models.DateField() 
    
    TIME_SLOTS = [('morning', '아침'), ('lunch', '점심'), ('dinner', '저녁')]
    time_slot = models.CharField(max_length=10, choices=TIME_SLOTS)
    
    is_taken = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_id', 'drug', 'date_to_take', 'time_slot')
