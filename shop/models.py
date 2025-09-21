from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    class Meta:
        permissions = [
            ("can_edit_product", "Can edit product"),
            ("can_view_product", "Can view product"),
        ]

    def __str__(self):
        return self.name