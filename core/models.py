from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    frequency = models.CharField(max_length=30, choices=FREQUENCY_CHOICES, default='daily')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    note = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('habit', 'date')
    
    def __str__(self):
        return f"{self.habit.name} - {self.date}"

class Partnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_partnerships')
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partner_of')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.partner.username}"
    
class Streak(models.Model):
    habit = models.OneToOneField(Habit, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_check_in = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.habit.name} - {self.current_streak} - {self.longest_streak}"