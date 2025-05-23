from djongo import models

# Create your models here.
class Products(models.Model):
    _id = models.ObjectIdField()
    name =  models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.CharField(max_length=50)
    tags = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name