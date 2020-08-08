from django.db import models


class investment(models.Model):
    mutual_fund_name = models.CharField(max_length=256, blank=False, null=False)
    investment_amount = models.IntegerField(blank=True, null=True)
    investment_date = models.DateField(blank=False, null=False)
    units = models.IntegerField(blank=True, null=True)
    withdraw_amount = models.FloatField(blank=True, null=True)
    withdraw_date = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
