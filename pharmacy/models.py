import os
import requests
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('tablet', 'Tablet'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('supplement', 'Supplement'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    # Healthcare Project Special Fields
    expiry_date = models.DateField(null=True, blank=True)
    requires_prescription = models.BooleanField(default=False)
    
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Agar image upload nahi hui hai tabhi auto-fetch chalega
        if not self.image:
            try:
                # Name ke pehle word se Wikipedia API par search karenge
                search_term = self.name.split()[0]
                api_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={search_term}&prop=pageimages&format=json&pithumbsize=500"
                res = requests.get(api_url, timeout=5).json()
                
                pages = res.get('query', {}).get('pages', {})
                img_url = None
                
                for key, value in pages.items():
                    if 'thumbnail' in value:
                        img_url = value['thumbnail']['source']
                        break
                
                # Agar Wikipedia par image milti hai toh download karenge
                if img_url:
                    img_res = requests.get(img_url, timeout=5)
                    if img_res.status_code == 200:
                        file_name = f"{self.name.lower().replace(' ', '_')}.jpg"
                        self.image.save(file_name, ContentFile(img_res.content), save=False)
            except Exception as e:
                print(f"Auto image fetch error: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    prescription = models.FileField(upload_to='prescriptions/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.medicine.name}"
    from django.db import models

class Prescription(models.Model):
    patient_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    prescription_file = models.FileField(upload_to='prescriptions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.uploaded_at.strftime('%Y-%m-%d')}"