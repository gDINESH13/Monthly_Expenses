from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass



class Income(models.Model):
    TypeoOfIncome=models.CharField(max_length=100)
    MoneyEarned=models.IntegerField()
    Date=models.DateField(default=None)
    EarnedBy=models.ForeignKey(User,on_delete=models.CASCADE,default=None,related_name='earned')
    def __str__(self):
        return f"user:{self.EarnedBy} type:{self.TypeoOfIncome} money:{self.MoneyEarned}"

class Expense(models.Model):
    TypeoOfExpense=models.CharField(max_length=100)
    MoneySpent=models.IntegerField()
    Date=models.DateField(default=None)
    SpentBy=models.ForeignKey(User,on_delete=models.CASCADE,default=None,related_name='spent')
    def __str__(self):
        return f"user:{self.SpentBy} type:{self.TypeoOfExpense} money:{self.MoneySpent}"



#class Revenue(models.Model):
#    client=models.ForeignKey(User,on_delete=models.CASCADE)
#    Date=models.DateTimeField()
#    MoneySpentThatDay=models.ManyToManyField(Expense,blank=True,related_name="spent_on")
#    MoneyEarnedThatDay=models.ManyToManyField(Income,blank=True,related_name="earned_on")