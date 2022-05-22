from statistics import mode
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    current_sales = models.IntegerField(default=0)
    total_sales = models.IntegerField(default=0)
    color_code = models.CharField(max_length=100, default='RED')
    progress = models.IntegerField(default=0)
    progress_label = models.CharField(max_length=100, default='At Risk')
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return str(self.id)
