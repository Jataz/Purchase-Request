from django.db import models
from django.contrib.auth.models import User

class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quotation(models.Model):
    purchase_request = models.ForeignKey(PurchaseRequest, related_name='quotations', on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=255)
    quotation_file = models.FileField(upload_to='quotations/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('Created', 'Created'),
        ('Completed', 'Completed'),
    ]

    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
