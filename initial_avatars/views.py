from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from initial_avatars.generator import AvatarGenerator, GRAVATAR_DEFAULT_SIZE

# Create your views here.
def avatar(request, username, size=GRAVATAR_DEFAULT_SIZE):
    user = get_object_or_404(User, username=username)
    avatar = AvatarGenerator(user, size=int(size)).get_avatar()
    return HttpResponse(avatar)
