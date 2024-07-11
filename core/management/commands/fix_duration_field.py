from django.core.management.base import BaseCommand
from core.models import WritingSession
import datetime

class Command(BaseCommand):
    help = 'Convert string duration to timedelta'

    def handle(self, *args, **kwargs):
        for session in WritingSession.objects.all():
            if isinstance(session.duration, str):
                duration_parts = session.duration.split(':')
                if len(duration_parts) == 3:
                    hours, minutes, seconds = map(int, duration_parts)
                    session.duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
                else:
                    session.duration = datetime.timedelta(0)
                session.save()
        self.stdout.write(self.style.SUCCESS('Successfully converted string durations to timedelta'))
