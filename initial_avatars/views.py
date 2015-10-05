from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import last_modified, etag
from initial_avatars.generator import AvatarGenerator, GRAVATAR_DEFAULT_SIZE
from datetime import date, timedelta

def last_modified_func(request, username, size=GRAVATAR_DEFAULT_SIZE):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    return AvatarGenerator(u, int(size)).last_modification()

@last_modified(last_modified_func)
def avatar(request, username, size=GRAVATAR_DEFAULT_SIZE):
    user = get_object_or_404(User, username=username)
    url = AvatarGenerator(user, size=int(size)).get_avatar_url()
    try:
        response = HttpResponseRedirect(url)
        response['Cache-Control'] = 'max-age=2592000'
        response['Expires'] = (date.today() + timedelta(days=31)).strftime('%a, %d %b %Y 20:00:00 GMT')
        return response
    except Exception, e:
        return HttpResponse('Not Found', status=404)
