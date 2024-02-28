from django.db import models
from django.utils import timezone
from datetime import date

class MembershipPlan(models.Model):
    mname = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField()

    def __str__(self):
        return self.mname
    
class Participant(models.Model):
    pname = models.CharField(max_length=100)
    id_card = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.pname

class AttendanceRecord(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.participant} - {self.date}"
    
class MembershipPurchase(models.Model):
    participant = models.OneToOneField('Participant', on_delete=models.CASCADE)
    membership_plan = models.ForeignKey('MembershipPlan', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)  # Automatically set to current date
    end_date = models.DateField(null=True, blank=True)  # Set based on membership plan duration

    def save(self, *args, **kwargs):
        # Check if the participant already has an active plan
        existing_plan = MembershipPurchase.objects.filter(participant=self.participant, end_date__gte=timezone.now()).first()

        if existing_plan:
            # Participant already has an active plan, don't save this new plan
            return

        # Calculate end date based on membership plan duration
        if self.end_date is None:
            self.end_date = self.start_date + timezone.timedelta(
                days=self.membership_plan.duration_months * 30)  # Assuming 30 days per month

        super().save(*args, **kwargs)

    def is_expired(self):
        return self.end_date and self.end_date < timezone.now().date()

    def __str__(self):
        return f"{self.participant.pname} - {self.membership_plan.mname} ({self.start_date} to {self.end_date})"
