from .models import Task
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User



def task_context(request):
    now = timezone.now()

    has_overdue = False  # default if user is not authenticated

    if request.user.is_authenticated:
        overdue_qs = Task.objects.filter(
            due_date__lt=now, is_complete=False, owner=request.user
        )
        has_overdue = overdue_qs.exists()

    return {'has_overdue': has_overdue}


# print("Overdue & Incomplete Tasks Count:", overdue_qs.count())
# print("Tasks:", list(overdue_qs.values("title", "due_date", "is_complete")))
