from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField, CurrencyField
from django.db.models.signals import post_save
from django.dispatch import receiver


class TotalSaved(models.Model):
    title = models.CharField(max_length=100)
    amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency="ZAR", default=0
    )

    def __str__(self):
        return f"{self.title} - {self.amount}"


class AddSavings(models.Model):
    amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency="ZAR", default=0
    )
    total_saved = models.ForeignKey(TotalSaved, on_delete=models.CASCADE)

    @receiver(post_save, sender=TotalSaved)
    def add_to_total_saved(sender, instance, **kwargs):
        total_saved = instance.total_saved
        total_saved.amount += instance.amount
        total_saved.save()


class SavingGoal(models.Model):
    STATUS_CHOICES = (
        ("locked", "Locked"),
        ("unlocked", "Unlocked"),
        ("completed", "Completed"),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="media/goal/", blank=True, null=True)
    url_link = models.URLField(blank=True)
    cost = MoneyField(
        max_digits=10, decimal_places=2, default_currency="ZAR", default=0
    )
    date_acquired = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="locked")
    total_saved = models.ForeignKey(TotalSaved, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.cost} - {self.status}"

    def is_unlocked(self):
        return self.total_saved.amount >= self.cost

    def save(self, *args, **kwargs):
        if self.status == "completed":
            post_save.connect(update_total_saved_amount, sender=SavingGoal)
        elif self.is_unlocked():
            self.status = "unlocked"
        else:
            self.status = "locked"
        super().save(*args, **kwargs)


def update_total_saved_amount(sender, instance, **kwargs):
    total_saved = instance.total_saved
    total_saved.amount = total_saved.amount - instance.cost
    total_saved.save()

    # post_save.connect(update_total_saved_amount, sender=SavingGoal)

    # If the saving goal has been completed then I need to update the total saved amount.
    #  if savinggoal is completed, the cost of that savinggoal will be subtracted from the total saved amount

    """
    if saving goal status == completed"
        then the cost of the saving goal should be subtracted from the total saved amount
        #  for this to happen I need to trigger a on_save for the 
    
    
        """
