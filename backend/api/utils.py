from django.contrib.auth.models import User


def get_user_by_name(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


# TODO: emails are not unique
def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def get_user(identifier):
    try:
        return User.objects.get(username=identifier)
    except User.DoesNotExist:
        try:
            return User.objects.get(email=identifier)
        except User.DoesNotExist:
            return None
