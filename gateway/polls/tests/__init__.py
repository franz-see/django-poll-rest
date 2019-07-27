import datetime

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def set_permissions_to_user(user, modelClass, permission_list):
    model_type = ContentType.objects.get_for_model(modelClass)
    permissions = [Permission.objects.get(
        content_type=model_type,
        codename=permission)
        for permission in permission_list]
    user.user_permissions.set(permissions)
