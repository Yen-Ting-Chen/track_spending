from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Record(models.Model):
    RECORD_TYPE = [('income', '收入'), ('expense', '支出')]
    PAYMENT_METHODS = [
        ('cash', '現金'),
        ('card', '信用卡'),
        ('Apple Pay', 'Apple Pay'),
        ('Line Pay', 'Line Pay'),
        ('bank', '匯款'),
        ('other', '其他'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    record_type = models.CharField(max_length=10, choices=RECORD_TYPE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"
