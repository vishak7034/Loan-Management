from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

class Loan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # yearly %
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[("ACTIVE", "Active"), ("CLOSED", "Closed")], default="ACTIVE")

    def save(self, *args, **kwargs):
        r = self.interest_rate / 100 / 12
        n = self.tenure
        self.total_interest = self.amount * ((1 + r) ** n - 1)
        self.total_amount = self.amount + self.total_interest
        self.monthly_installment = self.total_amount / n
        super().save(*args, **kwargs)