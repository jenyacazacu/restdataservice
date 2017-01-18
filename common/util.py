from django.contrib.auth import get_user_model

def create_admin(username='admin', password='admin'):
    user = get_user_model().objects.create(username=username,
                                           is_superuser=True,
                                           is_staff=True,
                                           is_active=True)
    user.set_password(password)
    user.save()
    return user
