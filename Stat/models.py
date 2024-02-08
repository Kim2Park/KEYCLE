from django.db import models

# Create your models here.
class Stat(models.Model):
	id = models.AutoField(primary_key = True)
	total = models.IntegerField()

	class Meta:
		# 모델의 내용이 변경 가능하면 Ture, 변경 불가능하면 False 
		managed = False
		db_table = 'Stats'