from django.db import models
class Form_13(models.Model):
   created_at = models.DateTimeField(auto_now_add=True)
   approved = models.BooleanField(default=False)
   Q10 = models.CharField()
   Question_11 = models.DateField()
   This_is_the_3rd_question_man2 = models.CharField()
   Sect_2_question_13 = models.CharField()
