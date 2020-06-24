from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect

def index(request):
    return HttpResponse('You\'re at the index. <a href="/secure">Secure</a>')

@login_required
def secure(request):
    now=request.user.username
    print (now)
    html = "<html><body>Welcome %s.<a href='/logout'>Logout</a></body></html>" % now
    return HttpResponse(html)

def get_logout_url(request):
    '''
    Return the url of the logout for keycloak
    '''
    keycloak_redirect_url = settings.OIDC_OP_LOGOUT_ENDPOINT or None
    return keycloak_redirect_url + "?redirect_uri=" + request.build_absolute_uri("/")


def keycloak_logout(request):
    '''
    Perform the logout of the app and redirect to keycloak
    '''
    logout_url = get_logout_url(request)
    auth.logout(request)
    return HttpResponseRedirect(logout_url)