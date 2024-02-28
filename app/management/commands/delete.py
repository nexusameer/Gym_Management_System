from django.core.management.base import BaseCommand
from app.models import Participant
class Command(BaseCommand):
    help = 'Deletes specified suggestions from the database'

    def handle(self, *args, **kwargs):
        Participant.objects.filter(name__in=['Rimsha Hamza', 'Amber Wood']).delete()
        self.stdout.write(self.style.SUCCESS('Suggestions deleted successfully.'))